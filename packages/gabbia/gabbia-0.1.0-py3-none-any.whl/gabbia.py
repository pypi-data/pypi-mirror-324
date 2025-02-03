#!/usr/bin/env python
#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright (c) 2024 - 2025 -- Lars Heuer
#
"""\
Gabbia: A Wayland kiosk.
"""
from __future__ import annotations

import argparse
import enum
import logging
import logging.handlers
import os
import shlex
import signal
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial, wraps
from itertools import chain
from pathlib import Path
from typing import Any, Protocol, cast, Final

from pywayland.protocol.wayland import WlKeyboard, WlSeat
from pywayland.server import Display, EventLoop, Listener, Signal

from wlroots import ffi, lib
from wlroots.util.edges import Edges
from wlroots.allocator import Allocator
from wlroots.backend import Backend
from wlroots.renderer import Renderer
from wlroots.util import log as wlroots_log
from wlroots.util.box import Box
from wlroots.util.clock import Timespec
from wlroots.wlr_types import server_decoration as server_deco
from wlroots.wlr_types.compositor import Compositor, SubCompositor, Surface
from wlroots.wlr_types.cursor import Cursor, WarpMode
from wlroots.wlr_types.data_control_v1 import DataControlManagerV1
from wlroots.wlr_types.data_device_manager import DataDeviceManager
from wlroots.wlr_types.export_dmabuf_v1 import ExportDmabufManagerV1
import wlroots.wlr_types.foreign_toplevel_management_v1 as ftm
from wlroots.wlr_types.gamma_control_v1 import GammaControlManagerV1
from wlroots.wlr_types.idle_inhibit_v1 import IdleInhibitorManagerV1, IdleInhibitorV1
from wlroots.wlr_types.idle_notify_v1 import IdleNotifierV1
from wlroots.wlr_types.input_device import InputDevice, InputDeviceType, ButtonState
from wlroots.wlr_types.keyboard import Keyboard, KeyboardKeyEvent, KeyboardModifier
from wlroots.wlr_types.layer_shell_v1 import LayerShellV1, LayerShellV1Layer, LayerSurfaceV1, \
    LayerSurfaceV1KeyboardInteractivity
from wlroots.wlr_types.output import Output, OutputState
try:
    from wlroots.wlr_types.output import OutputRequestStateEvent  # type: ignore
except ImportError:
    from wlroots.wlr_types.output import OutputEventRequestState as OutputRequestStateEvent
from wlroots.wlr_types.output_layout import OutputLayout
from wlroots.wlr_types.output_management_v1 import OutputConfigurationHeadV1, \
    OutputConfigurationV1, OutputManagerV1
from wlroots.wlr_types.pointer import Pointer, PointerAxisEvent, PointerButtonEvent,\
    PointerMotionAbsoluteEvent, PointerMotionEvent
from wlroots.wlr_types.presentation_time import Presentation
from wlroots.wlr_types.primary_selection_v1 import PrimarySelectionV1DeviceManager
from wlroots.wlr_types.relative_pointer_manager_v1 import RelativePointerManagerV1
from wlroots.wlr_types.scene import Scene, SceneBuffer, SceneLayerSurfaceV1, \
    SceneNodeType, SceneOutput, SceneOutputLayout, SceneSurface, SceneTree, SceneRect
from wlroots.wlr_types.screencopy_v1 import ScreencopyManagerV1
from wlroots.wlr_types.seat import PointerRequestSetCursorEvent, \
    RequestSetPrimarySelectionEvent, RequestSetSelectionEvent, Seat
from wlroots.wlr_types.single_pixel_buffer_v1 import SinglePixelBufferManagerV1
from wlroots.wlr_types.touch import Touch, TouchDownEvent, TouchMotionEvent, TouchUpEvent
from wlroots.wlr_types.viewporter import Viewporter
from wlroots.wlr_types.virtual_keyboard_v1 import VirtualKeyboardManagerV1, VirtualKeyboardV1
from wlroots.wlr_types.virtual_pointer_v1 import VirtualPointerManagerV1, \
    VirtualPointerV1NewPointerEvent
from wlroots.wlr_types.xcursor_manager import XCursorManager
from wlroots.wlr_types.xdg_activation_v1 import XdgActivationV1, \
    XdgActivationV1RequestActivateEvent
from wlroots.wlr_types.xdg_decoration_v1 import XdgDecorationManagerV1, \
    XdgToplevelDecorationV1, XdgToplevelDecorationV1Mode as XdgDecoMode
from wlroots.wlr_types.xdg_output_v1 import XdgOutputManagerV1
from wlroots.wlr_types.xdg_shell import XdgShell, XdgSurface, XdgSurfaceRole, \
    XdgToplevel, XdgToplevelWMCapabilities
from xkbcommon import xkb

_XWAYLAND_AVAILABLE = True
try:
    from wlroots.xwayland import XWayland, Surface as XWaylandSurface, SurfaceConfigureEvent
except ImportError:
    _XWAYLAND_AVAILABLE = False


__all__: Final = ['run', 'Config']

__version__: Final = '0.1.0'

_DEBUG: Final = False

logger: Final = logging.getLogger(__name__)

_WL_EVENT_HANGUP: Final = EventLoop.FdMask.WL_EVENT_HANGUP
_WL_EVENT_ERROR: Final = EventLoop.FdMask.WL_EVENT_ERROR

_KEY_PRESSED: Final = WlKeyboard.key_state.pressed
_KEY_XF86Switch_VT_1: Final = xkb.keysym_from_name('XF86Switch_VT_1')

_BTN_LEFT: Final = 0x110  # linux/input-event-codes.h
_BTN_PRESSED: Final = ButtonState.PRESSED

_XCB_STACK_MODE_ABOVE: Final = 0  # <https://xcb.freedesktop.org/manual/group__XCB____API.html>

_WM_CAPABILITIES: Final = XdgToplevelWMCapabilities.MAXIMIZE | XdgToplevelWMCapabilities.FULLSCREEN

_ALL_EDGES: Final = Edges.TOP | Edges.BOTTOM | Edges.LEFT | Edges.RIGHT

_DIM_COLOR: Final = '#000000cc'
_FULLSCREEN_COLOR: Final = '#000'


if not hasattr(Box, '__bool__'):
    # <https://github.com/flacjacket/pywlroots/issues/218>
    def _wlr_box_equal(box1: Box, box2: Box):
        return box1.x == box2.x and box1.y == box2.y and box1.width == box2.width and box1.height == box2.height

    setattr(Box, '__eq__', _wlr_box_equal)
    setattr(Box, '__bool__', lambda box: not lib.wlr_box_empty(box._ptr))


class ListenerAware(Protocol):
    """\
    Protocol to support the :func:`subscribe` and :func:`unsubscribe` functionality.
    """
    _listeners: list[Listener]


def subscribe(sig: Signal, callback: Callable):
    """\
    Adds a listener to the provided signal.

    The :class:`pywayland.server.Listener` is omitted from the `callback`.
    """
    @wraps(callback)
    def cb(_, *args):
        callback(*args)

    try:
        obj = callback.__self__  # type: ignore
    except AttributeError:  # partial object
        obj = callback.func.__self__  # type: ignore

    listener = Listener(cb)
    obj._listeners.append(listener)
    sig.add(listener)


def unsubscribe(obj: ListenerAware, sig: Signal | None = None):
    """\
    Unsubscribes the provided instance from a specific signal or removes
    all listeners.
    """
    listeners = reversed(obj._listeners[:]) if not sig else \
                    [li for li in obj._listeners if li._signal._ptr == sig._ptr]  # type: ignore
    for listener in listeners:
        listener.remove()


class Screen:
    """\
    Wrapper around a wlr Output.
    """
    __slots__ = ('__weakref__', '_listeners', '_server', 'scene_output', '_data_handle',
                 'output', 'area', 'view_area', 'layers', 'fullscreen_rect')

    def __init__(self, *, server: Server, output: Output, scene_output: SceneOutput,
                 fullscreen_rect: SceneRect, area: Box, view_area: Box):
        self._listeners: list[Listener] = []
        self._data_handle = ffi.new_handle(self)
        self._server = server
        self.output = output
        self.output.data = self._data_handle
        self.scene_output = scene_output
        self.layers: list[list[Layer]] = [[] for _ in range(len(LayerShellV1Layer))]
        self.area = area
        self.view_area = view_area
        self.fullscreen_rect: SceneRect = fullscreen_rect
        self.fullscreen_rect.node.data = self._data_handle
        self.fullscreen_rect.node.set_enabled(enabled=False)
        subscribe(output.destroy_event, self._on_output_destroy)
        subscribe(output.frame_event, self._on_output_frame)
        subscribe(output.request_state_event, self._on_output_request_state)

    def __repr__(self) -> str:
        if output := self.output:
            return f'Screen(name="{output.name}", make="{output.make}", '\
                   f'model="{output.model}", serial={output.serial}, '\
                   f'size={self.size}'
        return 'Screen (unavailable)'

    @property
    def is_enabled(self) -> bool:
        return self.output is not None and self.output.enabled

    @property
    def size(self) -> tuple[int, int]:
        return self.output._ptr.width, self.output._ptr.height

    def _on_output_destroy(self, _: Any):
        self._server._on_screen_destroy(self)
        unsubscribe(self)
        if output := self.output:
            output.data = None
        self.scene_output.destroy()
        self.fullscreen_rect.node.data = None
        self.fullscreen_rect = None  # type: ignore
        del self._data_handle

    def _on_output_frame(self, _: Any):
        self.scene_output.commit()
        self.scene_output.send_frame_done(Timespec.get_monotonic_time())

    def _on_output_request_state(self, event: OutputRequestStateEvent):
        logger.debug(f'Output request state {self}')
        self.output.commit(event.state)

    def arrange_layers(self):
        logger.debug(f'Arrange layers for {self}')
        if not self.is_enabled:
            return
        full_area = self.area
        usable_area = Box(x=self.area.x, y=self.area.y, width=self.area.width, height=self.area.height)
        for layer in reversed(LayerShellV1Layer):
            self._arrange_layer(layer, full_area, usable_area, exclusive=True)
        for layer in reversed(LayerShellV1Layer):
            self._arrange_layer(layer, full_area, usable_area, exclusive=False)
        self.view_area = Box(x=usable_area.x, y=usable_area.y, width=usable_area.width, height=usable_area.height)
        self._server.exclusive_layer = None
        for ls_layer in (LayerShellV1Layer.OVERLAY, LayerShellV1Layer.TOP):
            for layer in self.layers[ls_layer]:
                if layer.layer_surface.current.keyboard_interactive == LayerSurfaceV1KeyboardInteractivity.EXCLUSIVE:
                    self._server.exclusive_layer = layer
                    self._server.focus(layer)
                    return

    def _arrange_layer(self, layershell_layer: LayerShellV1Layer, full_area: Box, usable_area: Box, exclusive: bool):
        for layer in self.layers[layershell_layer]:
            state = layer.layer_surface.current
            if exclusive != (0 < state.exclusive_zone):
                continue
            layer.scene_layer.configure(full_area, usable_area)
            layer.width = state.desired_width
            layer.height = state.desired_height
            layer.popup_tree.node.set_position(layer.scene_tree.node.x, layer.scene_tree.node.y)


class WindowKind(enum.IntEnum):
    XDG = 1
    X11_MANAGED = 2
    X11_UNMANAGED = 3
    LAYER = 4


class Window(Protocol):
    """\
    Common interface for :class:`View` and :class:`Layer`.
    """

    @property
    def kind(self) -> WindowKind:
        ...

    @property
    def x(self) -> int:
        ...

    @property
    def y(self) -> int:
        ...

    @property
    def is_mapped(self) -> bool:
        ...

    @property
    def wlr_surface(self) -> Surface | None:
        ...

    @property
    def scene_tree(self) -> SceneTree | None:
        ...

    def is_transient_for(self, parent: Window) -> bool:
        ...


class View:
    """\
    Wrapper around a surface.

    A view can handle XDG surfaces and XWayland surfaces and provides a
    common API for both of them.

    To differentiate between them use the ``kind`` attribute.
    A XWayland surface may change from ``X11_MANAGED`` to ``X11_UNMANGED`` and
    vice versa.
    """
    __slots__ = ('__weakref__', '_listeners', '_data_handle', '_server',
                 '_surface', 'scene_tree', 'kind', '_activated',
                 '_ftm_handle', 'is_xdg', 'is_fullscreen', 'was_fullscreen',
                 '_dim_rect', 'title', 'app_id')

    def __init__(self, *, server: Server, surface: XdgSurface | XWaylandSurface,
                 is_xdg: bool = True):
        self._listeners: list[Listener] = []
        self._data_handle = ffi.new_handle(self)
        self._server = server
        surface.data = self._data_handle
        self._surface: XdgSurface | XWaylandSurface = surface
        self.scene_tree: SceneTree | None = None
        self._dim_rect: SceneRect | None = None
        self.kind = WindowKind.XDG if is_xdg else WindowKind.X11_MANAGED
        self._ftm_handle:  ftm.ForeignToplevelHandleV1 | None = None  # Set by the server
        self._activated = False
        self.is_xdg: Final = is_xdg
        self.is_fullscreen = False
        self.was_fullscreen = False
        self.title: str = ''
        self.app_id: str = ''
        subscribe(self._surface.destroy_event, self._on_surface_destroy)
        if is_xdg:
            xdg_surface = self.xdg_surface
            xdg_surface.surface.data = self._data_handle
            xdg_surface.set_wm_capabilities(_WM_CAPABILITIES)
            subscribe(xdg_surface.surface.commit_event, self._on_xdg_commit)
            subscribe(xdg_surface.surface.unmap_event, self._on_surface_unmap)
            subscribe(xdg_surface.surface.map_event, self._on_surface_map)
            subscribe(xdg_surface.toplevel.request_fullscreen_event, self._on_fullscreen_request)
        else:
            x11_surface = self.x11_surface
            if x11_surface.override_redirect:
                self.kind = WindowKind.X11_UNMANAGED
            subscribe(x11_surface.associate_event, self._on_x11_associate)
            subscribe(x11_surface.dissociate_event, self._on_x11_dissociate)
            subscribe(x11_surface.request_configure_event, self._on_x11_configure)
            subscribe(x11_surface.set_override_redirect_event, self._on_x11_override_redirect)
            subscribe(x11_surface.request_fullscreen_event, self._on_fullscreen_request)

    def __repr__(self) -> str:
        return f'View(is_main={self.is_main}, kind={self.kind.name}, '\
               f'title={self.title}, app_id={self.app_id}, is_mapped={self.is_mapped} '\
               f'activated={self.activated})'

    @property
    def xdg_surface(self) -> XdgSurface:
        assert self.is_xdg
        return cast(XdgSurface, self._surface)

    @property
    def x11_surface(self) -> XWaylandSurface:
        assert not self.is_xdg
        return cast(XWaylandSurface, self._surface)

    @property
    def wlr_surface(self) -> Surface | None:
        """\
        Returns the surface.

        This MUST return an instance of Surface iff the view is mapped,
        otherwise it MAY return ``None`` if the view is an X11 view.
        """
        return self._surface.surface if self._surface else None

    @property
    def is_mapped(self) -> bool:
        return self.wlr_surface._ptr.mapped if self.wlr_surface else False

    @property
    def activated(self) -> bool:
        return self._activated

    @activated.setter
    def activated(self, active: bool):
        if self._activated == active:
            return
        if self.is_xdg:
            xdg_surface = self.xdg_surface
            xdg_surface.set_activated(active)
        else:
            self.x11_surface.activate(active)
        self._activated = active
        if ftm_handle := self.ftm_handle:
            ftm_handle.set_activated(active)

    @property
    def x(self) -> int:
        assert self.scene_tree
        return self.scene_tree.node.x

    @property
    def y(self) -> int:
        assert self.scene_tree
        return self.scene_tree.node.y

    @property
    def ftm_handle(self) -> ftm.ForeignToplevelHandleV1 | None:
        return self._ftm_handle

    @ftm_handle.setter
    def ftm_handle(self, ftm_handle: ftm.ForeignToplevelHandleV1 | None):
        if prev_handle := self._ftm_handle:
            unsubscribe(self, prev_handle.request_close_event)
            unsubscribe(self, prev_handle.request_maximize_event)
            unsubscribe(self, prev_handle.request_fullscreen_event)
            unsubscribe(self, prev_handle.request_activate_event)
            prev_handle.destroy()
        self._ftm_handle = None
        if ftm_handle is not None:
            if self.is_mapped:
                self._ftm_handle = ftm_handle
                subscribe(ftm_handle.request_close_event, self._on_ftm_request_close)
                subscribe(ftm_handle.request_maximize_event, self._on_ftm_request_maximize)
                subscribe(ftm_handle.request_fullscreen_event, self._on_ftm_request_fullscreen)
                subscribe(ftm_handle.request_activate_event, self._on_ftm_request_activate)
                ftm_handle.set_app_id(self.app_id)
                ftm_handle.set_title(self.title)
                ftm_handle.set_activated(self.activated)
                if self.is_fullscreen:
                    ftm_handle.set_fullscreen(True)

    def close(self):
        if self.is_xdg:
            self.xdg_surface.send_close()
        else:
            self.x11_surface.close()

    def _on_xdg_commit(self, _: Any):
        if self.xdg_surface._ptr.initial_commit:
            self.xdg_surface.schedule_configure()
            if self.xdg_surface.toplevel.requested.fullscreen:
                self.fullscreen(True)
            else:
                self.place()

    def _on_surface_map(self, _: Any):
        parent_scene_tree = self._server.view_scene_tree
        if self.is_xdg:
            xdg_surface = self.xdg_surface
            self.scene_tree = Scene.xdg_surface_create(parent_scene_tree, xdg_surface)
            xdg_surface.set_tiled(_ALL_EDGES)
            toplevel = xdg_surface.toplevel
            subscribe(toplevel.set_title_event, self._on_set_title)
            subscribe(toplevel.set_app_id_event, self._on_set_app_id)
            title, app_id = toplevel.title, toplevel.app_id
        else:
            assert self.wlr_surface
            x11_surface = self.x11_surface
            self.scene_tree = SceneTree.subsurface_tree_create(parent_scene_tree, self.wlr_surface)
            x11_surface.set_maximized(True)
            subscribe(x11_surface.set_title_event, self._on_set_title)
            subscribe(x11_surface.set_class_event, self._on_set_app_id)
            title, app_id = x11_surface.title, x11_surface.wm_class
        if title:
            self.title = title
        if app_id:
            self.app_id = app_id
        if scene_tree := self.scene_tree:
            scene_tree.node.data = self._data_handle
            scene_tree.node.set_enabled()
            self._dim_rect = SceneRect(scene_tree, 0, 0, self._server.dim_color)
            self._dim_rect.node.set_enabled(enabled=False)
            self._dim_rect.node.data = self._data_handle
            self._server.view_map(self)
        else:
            msg = f'Failed to create scene tree for {self}'
            logger.error(msg)
            raise RuntimeError(msg)

    def _on_surface_unmap(self, _: Any):
        self._server.view_unmap(self)
        if self.is_xdg:
            toplevel = self.xdg_surface.toplevel
            unsubscribe(self, toplevel.set_title_event)
            unsubscribe(self, toplevel.set_app_id_event)
        else:
            x11_surface = self.x11_surface
            unsubscribe(self, x11_surface.set_title_event)
            unsubscribe(self, x11_surface.set_class_event)
        if dim_rect := self._dim_rect:
            dim_rect.node.data = None
            dim_rect.node.destroy()
            self._dim_rect = None
        if scene_tree := self.scene_tree:
            scene_tree.node.data = None
            scene_tree.node.destroy()
        self.scene_tree = None

    def _on_surface_destroy(self, _: Any):
        self._server.view_destroy(self)
        # Important to do it here before unsubscribe otherwise ftm_handle = None
        # tries to unsubscribe from events it is no longer subscribed to.
        self.ftm_handle = None
        unsubscribe(self)
        if wlr_surface := self.wlr_surface:
            wlr_surface.data = None
        self._surface.data = None
        self._surface = None  # type: ignore
        del self._data_handle

    def _on_x11_associate(self, _: Any):
        logger.debug(f'Associate {self}')
        if wlr_surface := self.wlr_surface:
            subscribe(wlr_surface.map_event, self._on_surface_map)
            subscribe(wlr_surface.unmap_event, self._on_surface_unmap)
        else:
            msg = f'No associated wlr surface for {self}'
            logger.error(msg)
            raise RuntimeError(msg)

    def _on_x11_dissociate(self, _: Any):
        logger.debug(f'Dissociate {self}')
        if wlr_surface := self.wlr_surface:
            unsubscribe(self, wlr_surface.map_event)
            unsubscribe(self, wlr_surface.unmap_event)

    def _on_x11_configure(self, event: SurfaceConfigureEvent):
        x11_surface = self.x11_surface
        if not x11_surface.surface or not self.is_mapped:
            x11_surface.configure(x=event.x, y=event.y, width=event.width, height=event.height)
            return
        if self.kind == WindowKind.X11_UNMANAGED:
            assert self.scene_tree
            self.scene_tree.node.set_position(event.x, event.y)
            x11_surface.configure(x=event.x, y=event.y, width=event.width, height=event.height)

    def _on_x11_override_redirect(self, _: Any):
        self.kind = WindowKind.X11_UNMANAGED if self.x11_surface.override_redirect else WindowKind.X11_MANAGED

    def _on_fullscreen_request(self, _: Any):
        logger.debug(f'Fullscreen request {self}')
        req = self.xdg_surface.toplevel.requested.fullscreen if self.is_xdg else self.x11_surface.fullscreen
        self.fullscreen(req)

    def fullscreen(self, fullscreen: bool):
        logger.debug(f'fullscreen enabled={fullscreen}')
        if not self.is_mapped:
            logger.debug(f'Unmapped surface requested fullscreen. Ignore request for {self}')
            return
        if self.is_fullscreen == fullscreen:
            return
        self.is_fullscreen = fullscreen
        self.was_fullscreen = fullscreen
        self._surface.set_fullscreen(fullscreen)
        parent_tree = self._server.fullscreen_scene_tree if fullscreen else self._server.view_scene_tree
        assert self.scene_tree
        assert self.scene_tree.node
        self.scene_tree.node.reparent(parent_tree)
        if screen := self._server.current_screen:
            screen.arrange_layers()
            output_box = screen.area if fullscreen else screen.view_area
            self.place(output_box.x, output_box.y, output_box.width, output_box.height)
            screen.fullscreen_rect.node.set_enabled(enabled=fullscreen)
        if ftm_handle := self.ftm_handle:
            ftm_handle.set_fullscreen(fullscreen)

    def _on_set_title(self, _: Any):
        title = self.xdg_surface.toplevel.title if self.is_xdg else self.x11_surface.title
        if not title:
            title = ''
        if self.title != title:
            self.title = title
            if ftm_handle := self.ftm_handle:
                ftm_handle.set_title(title)

    def _on_set_app_id(self, _: Any):
        app_id = self.xdg_surface.toplevel.app_id if self.is_xdg else self.x11_surface.wm_class
        if not app_id:
            app_id = ''
        if app_id != self.app_id:
            self.app_id = app_id
            if ftm_handle := self.ftm_handle:
                ftm_handle.set_app_id(app_id)

    def _on_ftm_request_close(self, _: Any):
        logger.debug('ftm close request')
        if not self.activated:
            return
        self.close()

    def _on_ftm_request_fullscreen(self, event: ftm.ForeignToplevelHandleV1FullscreenEvent):
        logger.debug('ftm fullscreen request')
        if not self.activated:
            return
        self.fullscreen(event.fullscreen)

    def _on_ftm_request_maximize(self, event: ftm.ForeignToplevelHandleV1MaximizedEvent):
        logger.debug('ftm maximize request')
        if not self.activated:
            return
        if event.maximized:
            self.fullscreen(False)

    def _on_ftm_request_activate(self, _: Any):
        logger.debug('ftm activation request')
        if self.activated:
            return
        self._server.focus(self)

    @property
    def is_main(self) -> bool:
        """\
        Returns if this view has no parent.
        """
        return (self.xdg_surface.toplevel.parent if self.is_xdg else self.x11_surface.parent) is None

    def geometry(self) -> Box:
        """\
        Returns the geometry of the view.
        """
        if self.is_xdg:
            return self.xdg_surface.get_geometry()
        surface = self.x11_surface
        return Box(x=surface.x, y=surface.y, width=surface.width, height=surface.height)

    def size(self) -> tuple[int, int]:
        """\
        Returns the width and height.
        """
        geo = self.geometry()
        return geo.width, geo.height

    def has_fixed_size(self) -> bool:
        """\
        Returns if this view has a fixed size (i.e. an About dialog).
        """
        size = self.xdg_surface.toplevel._ptr.current if self.is_xdg else self.x11_surface.size_hints
        if size:
            return 0 < size.min_width == size.max_width and 0 < size.min_height == size.max_height
        return False

    def place(self, x=0, y=0, width: int | None = None, height: int | None =  None, maximized=False):
        logger.debug(f'Place {self} to x={x}, y={y}, width={width}, height={height}, maximized={maximized}')
        if width and height:
            if self.is_xdg:
                xdg_surface = self.xdg_surface
                xdg_surface.set_size(width, height)
                xdg_surface.set_bounds(width, height)
            else:
                self.x11_surface.configure(x, y, width, height)
            self._surface.set_maximized(maximized)
            if dim_rect := self._dim_rect:
                dim_rect.set_size(width, height)
        if scene_tree := self.scene_tree:
            scene_tree.node.set_position(x, y)
        if ftm_handle := self._ftm_handle:
            ftm_handle.set_maximized(maximized)

    def is_transient_for(self, parent: Window) -> bool:
        if parent.kind == WindowKind.LAYER:
            return False
        parent = cast(View, parent)
        return self._xdg_is_transient_for(parent) if self.is_xdg else self._x11_is_transient_for(parent)

    def _x11_is_transient_for(self, parent: View) -> bool:
        if parent.is_xdg:
            return False
        surface: XWaylandSurface | None = self.x11_surface
        parent_surface = parent.x11_surface
        while surface:
            if surface.parent == parent_surface:
                return True
            surface = surface.parent
        return False

    def _xdg_is_transient_for(self, parent: View) -> bool:
        if not parent.is_xdg:
            return False
        toplevel: XdgToplevel | None = self.xdg_surface.toplevel
        parent_toplevel = parent.xdg_surface.toplevel
        while toplevel:
            if toplevel.parent == parent_toplevel:
                return True
            toplevel = toplevel.parent
        return False

    def dim(self, dim: bool):
        if dim_rect := self._dim_rect:
            dim_rect.node.set_enabled(enabled=dim)


class Layer:
    """\
    Layer shell surface.

    <https://wayland.app/protocols/wlr-layer-shell-unstable-v1>
    """
    __slots__ = ('__weakref__', '_listeners', '_data_handle', '_server',
                 'scene_layer', 'popup_tree', 'scene_tree', 'layer_surface',
                 'kind', 'index', 'width', 'height')

    def __init__(self, *, server: Server, layer_surface: LayerSurfaceV1,
                 scene_layer: SceneLayerSurfaceV1, popup_tree: SceneTree):
        assert layer_surface.output
        self._listeners: list[Listener] = []
        self._data_handle = ffi.new_handle(self)
        self._server = server
        self.scene_layer = scene_layer
        self.popup_tree: SceneTree = popup_tree
        self.popup_tree.node.data = self._data_handle
        self.scene_tree: SceneTree = self.scene_layer.tree
        self.scene_tree.node.data = self._data_handle
        self.layer_surface: LayerSurfaceV1 = layer_surface
        self.layer_surface.data = self._data_handle
        self.index = layer_surface.current.layer
        self.kind: Final = WindowKind.LAYER
        self.width: int = 0
        self.height: int = 0
        subscribe(layer_surface.surface.commit_event, self._on_commit)
        subscribe(layer_surface.surface.map_event, self._on_map)
        subscribe(layer_surface.surface.unmap_event, self._on_unmap)
        subscribe(layer_surface.destroy_event, self._on_destroy)
        subscribe(layer_surface.output.destroy_event, self._on_output_destroy)

    @property
    def x(self) -> int:
        return self.scene_tree.node.x

    @property
    def y(self) -> int:
        return self.scene_tree.node.y

    @property
    def wlr_surface(self) -> Surface:
        return self.layer_surface.surface

    @property
    def is_mapped(self) -> bool:
        return self.wlr_surface._ptr.mapped if self.wlr_surface else False

    def _on_destroy(self, _: Any):
        logger.debug(f'Layer destroy {self}')
        self._server.on_layer_destroy(self)
        unsubscribe(self)
        self.layer_surface.data = None
        self.layer_surface = None  # type: ignore
        self.popup_tree.node.data = None
        self.popup_tree.node.destroy()
        self.scene_tree.node.data = None
        self.scene_tree = None  # type: ignore
        del self._data_handle

    def _on_output_destroy(self, _: Any):
        self.close()

    def _on_map(self, _: Any):
        logger.debug(f'Layer map {self}')
        self.scene_tree.node.set_enabled(enabled=True)
        self.popup_tree.node.set_enabled(enabled=True)
        self._server.on_layer_map(self)

    def _on_unmap(self, _: Any):
        logger.debug(f'Layer unmap {self}')
        self._server.on_layer_unmap(self)
        self.scene_tree.node.set_enabled(enabled=False)
        self.popup_tree.node.set_enabled(enabled=False)

    def _on_commit(self, _: Any):
        # TODO: Evaluate the "committed" property <https://github.com/flacjacket/pywlroots/issues/221>
        layer_surface = self.layer_surface
        if not layer_surface.output or not layer_surface.output.data:
            return
        pending = layer_surface.pending
        if self.index != pending.layer or self.width != pending.desired_width \
            or self.height != pending.desired_height:
            parent_tree = self._server.layer_trees[pending.layer]
            self.scene_tree.node.reparent(parent_tree)
            self.popup_tree.node.reparent(parent_tree)
            if self.scene_tree.node.enabled:
                screen = cast(Screen, layer_surface.output.data)
                screen.layers[self.index].remove(self)
                screen.layers[pending.layer].append(self)
                self.index = pending.layer

    def close(self):
        # TODO <https://github.com/flacjacket/pywlroots/issues/224>
        #self.layer_surface.output = None
        self.layer_surface.destroy()

    def is_transient_for(self, parent: Window) -> bool:
        return False


def idle_activity(func: Callable):
    """\
    Decorator which signals activity to the idle notifier.

    Note: Expects that the 1st arg refers to an :class:`InputManager` instance.
    """
    @wraps(func)
    def inner(*args, **kw):
        cast(InputManager, args[0]).notify_activity()
        func(*args, **kw)
    return inner


def _get_keysyms(xkb_state, keycode) -> tuple[int]:
    syms_out = ffi.new('const xkb_keysym_t **')
    nsyms = lib.xkb_state_key_get_syms(xkb_state, keycode, syms_out)
    if nsyms > 0:
        assert syms_out[0] != ffi.NULL
    return tuple(syms_out[0][i] for i in range(nsyms))


class InputManager:
    """\
    Provides a wlr Seat and handles all input devices.
    """
    __slots__ = ('_listeners', '_server', '_session', '_config', 'cursor',
                 'xcursor_manager', '_pointer_manager',
                 '_virtual_keyboard_manager', '_virtual_pointer_manager',
                 '_seat', '_keyboards', '_keyboards_virtual', '_pointers',
                 '_pointers_virtual', '_touch', '_idle_notifier',
                 '_idle_inhibitor_manager', '_idle_inhibitors')

    def __init__(self, *, server: Server, config: InputConfig):
        self._listeners: list[Listener] = []
        self._server = server
        self._config = config
        self._session = self._server.backend.get_session()
        display = server.display
        seat = Seat(display, 'seat0')
        self._seat: Seat = seat
        cursor = Cursor(self._server.output_layout)
        self.cursor = cursor
        cursor_size = config.cursor_size
        self.xcursor_manager = XCursorManager(None, cursor_size)
        os.environ['XCURSOR_SIZE'] = str(cursor_size)
        self._pointer_manager = RelativePointerManagerV1(display)
        self._virtual_keyboard_manager = VirtualKeyboardManagerV1(display)
        self._virtual_pointer_manager = VirtualPointerManagerV1(display)
        self._idle_notifier = IdleNotifierV1(display)
        self._idle_inhibitor_manager = IdleInhibitorManagerV1(display)
        self._keyboards: list[Keyboard] = []
        self._keyboards_virtual: list[Keyboard] = []
        self._pointers: list[Pointer] = []
        self._pointers_virtual: list[Pointer] = []
        self._touch: list[Touch] = []
        self._idle_inhibitors: int = 0
        subscribe(seat.request_set_cursor_event, self._on_pointer_request_cursor)
        subscribe(seat.request_set_selection_event, self._on_request_set_selection)
        subscribe(seat.request_set_primary_selection_event, self._on_request_set_primary_selection)
        subscribe(self._server.backend.new_input_event, self._on_input_new)
        subscribe(self._virtual_keyboard_manager.new_virtual_keyboard_event, self._on_virtual_keyboard_new)
        subscribe(self._virtual_pointer_manager.new_virtual_pointer_event, self._on_virtual_pointer_new)
        subscribe(cursor.motion_event, self._on_cursor_motion)
        subscribe(cursor.motion_absolute_event, self._on_cursor_motion_absolute)
        subscribe(cursor.axis_event, self._on_cursor_axis)
        subscribe(cursor.frame_event, self._on_cursor_frame)
        subscribe(cursor.button_event, self._on_cursor_button)
        subscribe(cursor.touch_down_event, self._on_touch_down)
        subscribe(cursor.touch_up_event, self._on_touch_up)
        subscribe(cursor.touch_motion_event, self._on_touch_motion)
        subscribe(cursor.touch_frame_event, self._on_touch_frame)
        subscribe(self._idle_inhibitor_manager.new_inhibitor_event, self._on_idle_inhibitor_new)

    def terminate(self):
        """\
        Releases all resources occupied by this instance.
        """
        unsubscribe(self)
        self._seat.set_keyboard(None)
        self.xcursor_manager.destroy()
        self.cursor.destroy()
        self._seat.destroy()
        self._seat = None  # type: ignore

    @property
    def seat(self) -> Seat | None:
        return self._seat if self._seat and not self._seat.destroyed else None

    @property
    def focused_surface(self) -> Surface | None:
        return self.focused_surface_keyboard() or self.focused_surface_pointer()

    def focused_surface_keyboard(self) -> Surface | None:
        if self._seat is None:
            return None
        return self._seat.keyboard_state.focused_surface

    def focused_surface_pointer(self) -> Surface | None:
        if self._seat is None:
            return None
        return self._seat.pointer_state.focused_surface


    def maybe_clear_keyboard_focus(self, surface: Surface | None):
        if seat := self.seat:
            if surface == seat.keyboard_state.focused_surface:
                seat.keyboard_clear_focus()

    def maybe_clear_pointer_focus(self, surface: Surface | None):
        if seat := self.seat:
            if surface == seat.pointer_state.focused_surface:
                seat.pointer_clear_focus()

    def center_cursor(self, width: int, height: int):
        self.warp_pointer(width / 2, height / 2)

    def warp_pointer(self, x: float, y: float):
        self.cursor.warp(WarpMode.LayoutClosest, x, y)

    def _on_input_new(self, device: InputDevice):
        """\
        Called if a new input device (keyboard, mouse, …) was detected.
        """
        logger.debug(f'New input device {device.type.name}, {device.name}')
        match device.type:
            case InputDeviceType.KEYBOARD:
                self._keyboard_setup(Keyboard.from_input_device(device))
            case InputDeviceType.POINTER:
                self._pointer_setup(Pointer.from_input_device(device))
            case InputDeviceType.TOUCH:
                self._touch_setup(Touch.from_input_device(device))
            case _:
                logger.info(f'Unsupported input device: {device.type.name}')

    def _keyboard_setup(self, keyboard: Keyboard, virtual=False):
        """\
        Configures the provided keyboard and adds it to the known keyboards.
        """
        logger.debug(f'Setup keyboard: {keyboard} {"(virtual)" if virtual else ""}')
        config = self._config
        keyboard.set_repeat_info(config.keyboard_rate, config.keyboard_delay)
        xkb_ctx = xkb.Context()
        keymap = xkb_ctx.keymap_new_from_names(layout=config.keyboard_layout,
                                               variant=config.keyboard_variant,
                                               options=config.keyboard_options)
        keyboard.set_keymap(keymap)
        subscribe(keyboard.base.destroy_event, partial(self._on_keyboard_destroy, keyboard))
        subscribe(keyboard.key_event, partial(self._on_keyboard_key, keyboard))
        subscribe(keyboard.modifiers_event, partial(self._on_keyboard_modifiers, keyboard))
        keyboards = self._keyboards if not virtual else self._keyboards_virtual
        keyboards.append(keyboard)
        self._seat.set_keyboard(keyboard)
        self._update_capabilities()

    def _on_keyboard_destroy(self, keyboard: Keyboard, _: InputDevice):
        unsubscribe(self, keyboard.base.destroy_event)
        unsubscribe(self, keyboard.key_event)
        unsubscribe(self, keyboard.modifiers_event)
        try:
            self._keyboards.remove(keyboard)
        except ValueError:
            self._keyboards_virtual.remove(keyboard)
        seat = self._seat
        if seat.get_keyboard() == keyboard:
            kb = next(chain(reversed(self._keyboards),
                            reversed(self._keyboards_virtual)), None)
            seat.set_keyboard(kb)
        self._update_capabilities()

    @idle_activity
    def _on_keyboard_modifiers(self, keyboard: Keyboard, _: Any):
        seat = self._seat
        seat.set_keyboard(keyboard)
        seat.keyboard_notify_modifiers(keyboard.modifiers)

    @idle_activity
    def _on_keyboard_key(self, keyboard: Keyboard, event: KeyboardKeyEvent):
        modifier = keyboard.modifier
        handled = False
        if self._config.allow_vt_change and event.state == _KEY_PRESSED:
            keycode = event.keycode + 8
            keysyms = _get_keysyms(keyboard._ptr.xkb_state, keycode)
            handle_keybinding = partial(self._handle_keybinding, modifier)
            handled = any(map(handle_keybinding, keysyms))
        if not handled:
            seat = self._seat
            seat.set_keyboard(keyboard)
            seat.keyboard_notify_key(event)

    def _handle_keybinding(self, _: KeyboardModifier, keysym: int) -> bool:
        if 0 < keysym - _KEY_XF86Switch_VT_1 + 1 < 13:
            return self._session.change_vt(keysym - _KEY_XF86Switch_VT_1 + 1)
        return False

    def _touch_setup(self, touch: Touch):
        logger.debug(f'Touch setup {touch}')
        self._touch.append(touch)
        subscribe(touch.base.destroy_event, partial(self._on_touch_destroy, touch))
        self.cursor.attach_input_device(touch.base)
        self._map_input_to_output(touch)
        self._update_capabilities()

    def _on_touch_destroy(self, touch: Touch, _: InputDevice):
        unsubscribe(self,touch.base.destroy_event)
        self._touch.remove(touch)
        self.cursor.detach_input_device(touch.base)
        self._update_capabilities()

    def _pointer_setup(self, pointer: Pointer, virtual=False):
        logger.debug(f'Adding new pointer: "{pointer}", virtual={virtual}')
        pointers = self._pointers if not virtual else self._pointers_virtual
        pointers.append(pointer)
        subscribe(pointer.base.destroy_event, partial(self._on_pointer_destroy, pointer))
        self.cursor.attach_input_device(pointer.base)
        self._map_input_to_output(pointer)
        self._update_capabilities()

    def _on_pointer_destroy(self, pointer: Pointer, _: InputDevice):
        unsubscribe(self, pointer.base.destroy_event)
        try:
            self._pointers.remove(pointer)
        except ValueError:
            self._pointers_virtual.remove(pointer)
        self.cursor.detach_input_device(pointer.base)
        self._update_capabilities()

    def _on_virtual_keyboard_new(self, keyboard: VirtualKeyboardV1):
        self._keyboard_setup(Keyboard.from_input_device(keyboard.keyboard.base), virtual=True)

    def _on_virtual_pointer_new(self, event: VirtualPointerV1NewPointerEvent):
        pointer = Pointer.from_input_device(event.new_pointer.pointer.base)
        # TODO: <https://github.com/flacjacket/pywlroots/issues/217>
        self._pointer_setup(pointer, virtual=True)

    def _on_pointer_request_cursor(self, event: PointerRequestSetCursorEvent):
        if event._ptr.seat_client == self._seat.pointer_state._ptr.focused_client:
            self.cursor.set_surface(event.surface, event.hotspot)

    @idle_activity
    def _on_touch_down(self, event: TouchDownEvent):
        lx, ly = self.cursor.absolute_to_layout_coords(event.touch.base,
                                                       event.x, event.y)
        _, surface, sx, sy = self._server.window_at(lx, ly)
        serial = 0
        if surface:
            serial = self._seat.touch_notify_down(surface, event.time_msec,
                                                  event.touch_id, sx, sy)
        if serial and self._seat.touch_num_points() == 1:
            self._maybe_focus_window(lx, ly, _BTN_LEFT, _BTN_PRESSED)

    @idle_activity
    def _on_touch_up(self, event: TouchUpEvent):
        if not self._seat.touch_get_point(event.touch_id):
            return
        self._seat.touch_notify_up(event.time_msec, event.touch_id)

    @idle_activity
    def _on_touch_motion(self, event: TouchMotionEvent):
        if not self._seat.touch_get_point(event.touch_id):
           return
        lx, ly = self.cursor.absolute_to_layout_coords(event.touch.base,
                                                       event.x, event.y)
        _, surface, sx, sy = self._server.window_at(lx, ly)
        if surface:
            self._seat.touch_point_focus(time_msec=event.time_msec,
                                         surface=surface, touch_id=event.touch_id,
                                         surface_x=sx, surface_y=sy)
            self._seat.touch_notify_motion(time_msec=event.time_msec,
                                           touch_id=event.touch_id,
                                           surface_x=sx, surface_y=sy)
        else:
            self._seat.touch_point_clear_focus(time_msec=event.time_msec,
                                               touch_id=event.touch_id)  # type: ignore

    def _on_touch_frame(self, _: Any):
        self._seat.touch_notify_frame()

    @idle_activity
    def _on_cursor_motion(self, event: PointerMotionEvent):
        dx, dy = event.delta_x, event.delta_y
        self.cursor.move(dx, dy, input_device=event.pointer.base)
        self._cursor_motion_process(event.time_msec, dx, dy,
                                    event.unaccel_delta_x, event.unaccel_delta_y)

    @idle_activity
    def _on_cursor_motion_absolute(self, event: PointerMotionAbsoluteEvent):
        lx, ly = self.cursor.absolute_to_layout_coords(event.pointer.base, event.x, event.y)
        delta_x, delta_y = lx - self.cursor.x, ly - self.cursor.y
        self.cursor.warp(WarpMode.AbsoluteClosest, event.x, event.y, input_device=event.pointer.base)
        self._cursor_motion_process(event.time_msec, delta_x, delta_y, delta_x, delta_y)

    def _cursor_motion_process(self, time: int, delta_x: float, delta_y: float,
                               delta_x_unaccel: float, deta_y_unaccel: float):
        window, surface, sx, sy = self._server.window_at(self.cursor.x, self.cursor.y)
        if window is None:
            self.cursor.set_xcursor(self.xcursor_manager, self._config.cursor_theme)
        seat = self._seat
        if surface is None:
            # Clear pointer focus so future button events and such are not sent
            # to the last client to have the cursor over it.
            seat.pointer_clear_focus()
        else:
            seat.pointer_notify_enter(surface, sx, sy)
            seat.pointer_notify_motion(time, sx, sy)
        self._pointer_manager.send_relative_motion(self._seat, time * 1000, delta_x, delta_y,
                                                   delta_x_unaccel, deta_y_unaccel)

    def _on_cursor_axis(self, event: PointerAxisEvent):
        self._seat.pointer_notify_axis(event.time_msec, event.orientation,
                                       event.delta, event.delta_discrete, event.source)

    def _on_cursor_frame(self, _: Any):
        self._seat.pointer_notify_frame()

    @idle_activity
    def _on_cursor_button(self, event: PointerButtonEvent):
        self._seat.pointer_notify_button(event.time_msec, event.button, event.button_state)
        self._maybe_focus_window(self.cursor.x, self.cursor.y, event.button, event.button_state)

    def _maybe_focus_window(self, x, y, button: int, button_state: ButtonState):
        if button != _BTN_LEFT or button_state != _BTN_PRESSED:
            return
        if next_window := self._server.window_at(x, y)[0]:
            if focused_surface := self.focused_surface:
                focused_window = cast(Window, focused_surface.data)
                if focused_window is None:
                    return
                if focused_window == next_window or not focused_window.is_transient_for(next_window):
                    return
            self._server.focus(next_window)

    def _map_input_to_output(self, device: Pointer | Touch):
        """\
        Maps the provided input device to an output iff the input device provides
        a preferred output name.
        """
        if not device.output_name:
            return
        name = device.output_name
        output = next((s.output for s in self._server.screens if s.output.name == name), None)
        if output:
            self.cursor.map_input_to_output(device.base, output)

    def _update_capabilities(self):
        """\
        Updates the input device capabilities of the seat and the cursor
        accordingly.
        """
        has_pointers = any(chain(self._pointers, self._pointers_virtual))
        caps = WlSeat.capability.pointer
        if any(chain(self._keyboards, self._keyboards_virtual)):
            caps |= WlSeat.capability.keyboard
        if self._touch:
            caps |= WlSeat.capability.touch
        # Capabilties == 0 is treated as an error, keep pointer even if no pointer is attached
        if not has_pointers and caps ^ WlSeat.capability.pointer > 0:
            caps ^= WlSeat.capability.pointer
        self._seat.set_capabilities(caps)
        if has_pointers:
            self.cursor.set_xcursor(self.xcursor_manager, self._config.cursor_theme)
        else:
            # TODO: <https://github.com/flacjacket/pywlroots/issues/213>
            # self.cursor.unset_image()
            self._seat.pointer_notify_clear_focus()

    def _on_request_set_selection(self, event: RequestSetSelectionEvent):
        self._seat.set_selection(event._ptr.source, event.serial)

    def _on_request_set_primary_selection(self, event: RequestSetPrimarySelectionEvent):
        self._seat.set_primary_selection(event._ptr.source, event.serial)

    def _on_idle_inhibitor_new(self, idle_inhibitor: IdleInhibitorV1):
        logger.debug('Idle inhibitor new inhibitor')
        subscribe(idle_inhibitor.destroy_event, partial(self._on_idle_inhibitor_destroy,
                                                        idle_inhibitor))
        self._idle_inhibitors += 1
        self._check_idle_inhibitors()

    def _on_idle_inhibitor_destroy(self, idle_inhibitor: IdleInhibitorV1, _: Any):
        logger.debug('Idle inhibitor destroy')
        self._idle_inhibitors -= 1
        unsubscribe(self, idle_inhibitor.destroy_event)
        self._check_idle_inhibitors()

    def _check_idle_inhibitors(self):
        self._idle_notifier.set_inhibited(bool(self._idle_inhibitors))

    def notify_activity(self):
        self._idle_notifier.notify_activity(self._seat)


def _rgba(hex: str) -> tuple[float, float, float, float]:
    """\
    Converts a hexadecimal color into a RGBA tuple of floats.
    """
    hex = hex.lstrip('#')
    if len(hex) not in (3, 6, 8):
        raise ValueError(f'Invalid hex color, must be 3, 6, or 8 characters long, got "{hex}"')
    res = [int(i, 16) * 17 for i in hex] if len(hex) == 3 else [int(i, 16) for i in (hex[0:2], hex[2:4], hex[4:6])]
    res.append(int(hex[6:8], 16) if len(hex) == 8 else 255)
    return tuple(i / 255.0 for i in res)  # type: ignore


class Server:
    """\
    Server of Gabbia.

    Handles the main resources of Wayland.
    """
    __slots__ = ('_listeners', '_config', 'display', 'backend', '_renderer',
                 '_allocator', '_compositor', '_subcompositor', '_input_manager',
                 '_xdg_shell', '_layer_shell', '_scene', 'output_layout',
                 '_output_manager', '_xwayland', 'current_screen', '_layers',
                 'exclusive_layer', 'screens', '_views', '_app', 'view_scene_tree',
                 '_event_loop', '_ft_manager', '_is_quitting', '_data_handle',
                 '_app_result', '_scene_output_layout', 'layer_trees',
                 'view_scene_tree', 'fullscreen_scene_tree', 'dim_color',
                 '_fullscreen_color')

    def __init__(self, config: Config):
        self._listeners: list[Listener] = []
        self._app_result = 0
        self._xwayland = None
        self._is_quitting = False
        self._data_handle = ffi.new_handle(self)
        self._config = config
        self.display = Display()
        self._event_loop = self.display.get_event_loop()
        self.backend = Backend(self.display)
        self._renderer = Renderer.autocreate(self.backend)
        self._renderer.init_display(self.display)
        self._allocator = Allocator.autocreate(backend=self.backend, renderer=self._renderer)
        self._compositor = Compositor(self.display, renderer=self._renderer, version=5)
        self._subcompositor = SubCompositor(self.display)
        self._scene = Scene()
        self.output_layout = OutputLayout()
        self._scene_output_layout: SceneOutputLayout = self._scene.attach_output_layout(self.output_layout)  # type: ignore
        if not self._scene_output_layout:
            raise RuntimeError('SceneOutputLayout cannot be created')
        self._input_manager = InputManager(server=self, config=config)
        self._xdg_shell = XdgShell(self.display)
        self._layer_shell = LayerShellV1(self.display, version=4)
        self._output_manager = OutputManagerV1(self.display)
        self._ft_manager = ftm.ForeignToplevelManagerV1.create(self.display) if config.ftm else None
        self.screens: list[Screen] = []
        self.current_screen: Screen | None = None
        self.layer_trees = [SceneTree.create(self._scene.tree) for _ in range(6)]
        self.fullscreen_scene_tree = self.layer_trees.pop(4)  # scene tree between top and overlay
        self.view_scene_tree = self.layer_trees.pop(2)  # scene tree between bottom and top
        try:
            fs_color = _rgba(config.fullscreen_color)
        except ValueError:
            logger.info(f'Invalid fullscreen color "{config.fullscreen_color}". Use default fullscreen color')
            fs_color = _rgba(_FULLSCREEN_COLOR)
        self._fullscreen_color: Final = fs_color
        self._views: list[View] = []
        self._layers: set[Layer] = set()
        self.exclusive_layer: Layer | None = None
        self._app: subprocess.Popen | None = None
        try:
            dim_color = _rgba(config.dim_color)
        except ValueError:
            logger.info(f'Invalid dim color "{config.dim_color}". Use default dim color')
            dim_color = _rgba(_DIM_COLOR)
        self.dim_color: Final = dim_color
        subscribe(self.backend.new_output_event, self._on_output_new)
        subscribe(self.output_layout.change_event, self._on_output_layout_change)
        subscribe(self._output_manager.apply_event, partial(self._outputs_reconfigure, apply=True))
        subscribe(self._output_manager.test_event, partial(self._outputs_reconfigure, apply=False))
        subscribe(self._layer_shell.new_surface_event, self._on_layer_surface_new)
        subscribe(self._xdg_shell.new_surface_event, self._on_xdg_surface_new)

        if not config.no_x and _XWAYLAND_AVAILABLE:
            self._xwayland = XWayland(self.display, self._compositor, lazy=True)  # type: ignore
            subscribe(self._xwayland.ready_event, self._on_xwayland_ready)
            subscribe(self._xwayland.new_surface_event, partial(self._surface_new, is_xdg=False))
            os.environ['DISPLAY'] = self._xwayland.display_name or ''
            logger.debug(f'XWayland DISPLAY="{os.environ["DISPLAY"]}"')
        else:
            os.environ.pop('DISPLAY', None)

        self._event_loop.add_signal(signal.SIGINT, self._handle_signal)
        self._event_loop.add_signal(signal.SIGTERM, self._handle_signal)

        os.environ['XDG_CURRENT_DESKTOP'] = 'Gabbia'
        if False:
            os.environ['MOZ_ENABLE_WAYLAND'] = '1'
            os.environ['QT_QPA_PLATFORM'] = 'wayland'
            os.environ['GDK_BACKEND'] = 'wayland'
            os.environ['SDL_VIDEODRIVER'] = 'wayland'
            os.environ['ELECTRON_OZONE_PLATFORM_HINT'] = 'wayland'

    def run(self, cmd: str | list[str]) -> int:
        """\
        Runs the server: Sets up the socket and runs the Wayland display.

        :raises RuntimeException: In case of an error.
        :raises OSError: In case the `cmd` cannot be run.
        """
        display = self.display
        backend = self.backend
        presentation = Presentation.create(display, backend)
        self._scene.set_presentation(presentation)
        deco_mode = server_deco.ServerDecorationManagerMode.SERVER
        if not self._config.ssd:
            deco_mode = server_deco.ServerDecorationManagerMode.CLIENT
        deco_manager = server_deco.ServerDecorationManager.create(display)
        deco_manager.set_default_mode(deco_mode)
        xdg_decoration_manager = XdgDecorationManagerV1.create(display)
        subscribe(xdg_decoration_manager.new_toplevel_decoration_event, self._on_toplevel_decoration_new)
        XdgOutputManagerV1(display, self.output_layout)
        ExportDmabufManagerV1(display)
        DataDeviceManager(display)
        ScreencopyManagerV1(display)
        DataControlManagerV1(display)
        GammaControlManagerV1(display)
        PrimarySelectionV1DeviceManager(display)
        SinglePixelBufferManagerV1(display)
        Viewporter(display)
        xdg_activation = XdgActivationV1.create(display)
        subscribe(xdg_activation.request_activate_event, self._on_xdg_activation)
        socket = None
        if not self._config.default_wayland_socket:
            # Avoid using "wayland-0" as display socket
            # Background: <https://gitlab.freedesktop.org/wayland/weston/-/merge_requests/486>
            for i in range(1, 33):
                name_candidate = f'wayland-{i}'
                # <https://github.com/flacjacket/pywayland/issues/54>
                try:
                    display.add_socket(name_candidate)
                except Exception:
                    continue  # Socket in use
                socket = name_candidate
                break
        else:
            socket = display.add_socket().decode()
        if not socket:
            backend.destroy()
            raise RuntimeError('Unable to create a socket')
        logger.info(f'Listening on {socket}')
        os.environ['WAYLAND_DISPLAY'] = socket
        if not backend.start():
            backend.destroy()
            display.destroy()
            raise RuntimeError('Cannot start backend')
        try:
            self._app_spawn(cmd)
        except OSError as ex:
            raise ex
        output_box = self.current_screen.view_area  # type: ignore
        self._input_manager.center_cursor(width=output_box.width, height=output_box.height)
        display.run()
        self._cleanup()
        return self._app_result

    def quit(self):
        if self._is_quitting:
            return
        self._is_quitting = True
        self.display.terminate()

    def _cleanup(self):
        unsubscribe(self)
        if app := self._app:
            app.terminate()
        if xwayland := self._xwayland:
            xwayland.destroy()
        self.output_layout.destroy()
        self.display.flush_clients()
        for layer in set(self._layers):
            layer.close()
        for view in [view for view in reversed(self._views) if view.is_mapped]:
            view.close()
        self._input_manager.terminate()
        self.backend.destroy()
        self.display.destroy()

    def window_at(self, x: float, y: float) -> tuple[Window | None, Surface | None, float, float]:
        """\
        Returns the view at the provided coordinates.
        """
        nothing = None, None, 0, 0
        if (tmp := self._scene.tree.node.node_at(x, y)) is None:
            return nothing
        node, sx, sy = tmp
        if node.type != SceneNodeType.BUFFER:
            return nothing
        if (scene_buffer := SceneBuffer.from_node(node)) is None:
            return nothing
        if (scene_surface := SceneSurface.from_buffer(scene_buffer)) is None:
            return nothing
        surface = scene_surface.surface
        tree = cast(SceneTree, node.parent)
        while tree.node.data is None:
            tree = cast(SceneTree, tree.node.parent)
        return tree.node.data, surface, sx, sy

    def _on_toplevel_decoration_new(self, decoration: XdgToplevelDecorationV1):
        decoration.set_mode(XdgDecoMode.SERVER_SIDE if self._config.ssd else XdgDecoMode.CLIENT_SIDE)

    def _on_layer_surface_new(self, layer_surface: LayerSurfaceV1):
        logger.debug('Event: LayerShell new_surface_event')
        if not layer_surface.output and self.current_screen:
            layer_surface.output = self.current_screen.output
        if not layer_surface.output or not layer_surface.output.data:
            logger.debug('Cannot find output the layer is referring to. Ignore request')
            layer_surface.destroy()
            return
        screen = cast(Screen, layer_surface.output.data)
        parent_tree = self.layer_trees[layer_surface.current.layer]
        scene_layer = Scene.layer_surface_v1_create(parent_tree, layer_surface)
        popup_tree = SceneTree.create(parent_tree)
        layer = Layer(server=self, layer_surface=layer_surface,
                      scene_layer=scene_layer, popup_tree=popup_tree)
        self._layers.add(layer)
        screen.layers[layer.index].append(layer)
        screen.arrange_layers()
        self._update_view_positions()

    def on_layer_map(self, layer: Layer):
        assert layer.layer_surface.output
        screen = cast(Screen, layer.layer_surface.output.data)
        screen.arrange_layers()
        self._update_view_positions()

    def on_layer_unmap(self, layer: Layer):
        if self.exclusive_layer == layer:
            self.exclusive_layer = None
        assert layer.layer_surface.output
        screen = cast(Screen, layer.layer_surface.output.data)
        screen.layers[layer.index].remove(layer)
        screen.arrange_layers()
        if layer.wlr_surface == self._input_manager.focused_surface:
            self._input_manager.maybe_clear_keyboard_focus(layer.wlr_surface)
            view = next((view for view in reversed(self._views) if view.is_mapped), None)
            if view:
                self.focus(view)

    def on_layer_destroy(self, layer: Layer):
        self._layers.remove(layer)

    def _on_xdg_surface_new(self, xdg_surface: XdgSurface):
        if xdg_surface.role == XdgSurfaceRole.TOPLEVEL:
            self._surface_new(xdg_surface)
        elif xdg_surface.role == XdgSurfaceRole.POPUP:
            self._xdg_popup_new(xdg_surface)

    def _surface_new(self, surface: XdgSurface | XWaylandSurface, is_xdg: bool = True):
        logger.debug(f'New surface {surface} is_xdg={is_xdg}')
        view = View(server=self, surface=surface, is_xdg=is_xdg)
        self._views.append(view)
        logger.debug(f'New (unmapped) view {view}')

    def _xdg_popup_new(self, xdg_surface: XdgSurface):
        logger.debug(f'New popup {xdg_surface}, parent view: {xdg_surface.popup.parent.data}')
        parent_surface = xdg_surface.popup.parent
        window: Window | None = None
        if parent_xdg_surface := XdgSurface.try_from_surface(parent_surface):
            while parent_xdg_surface and parent_xdg_surface.role == XdgSurfaceRole.POPUP:
                parent_xdg_surface = XdgSurface.try_from_surface(parent_xdg_surface.popup.parent)
            assert parent_xdg_surface
            window = cast(View, parent_xdg_surface.data)
            assert window.scene_tree
            popup_scene_tree = Scene.xdg_surface_create(window.scene_tree, xdg_surface)
            xdg_surface.data = popup_scene_tree
        elif parent := LayerSurfaceV1.try_from_wlr_surface(parent_surface):
            window = cast(Layer, parent.data)
            self._scene.xdg_surface_create(window.popup_tree, xdg_surface)
        else:
            logger.warning('Unknown parent surface for popup')
            return
        assert window
        output_layout = self.output_layout
        output_box = xdg_surface.get_geometry()
        x, y = output_layout.closest_point(window.x + output_box.x,
                                           window.y + output_box.y)
        output_box = output_layout.get_box(output_layout.output_at(x, y))
        xdg_surface.popup.unconstrain_from_box(Box(x=round(output_box.x - x),
                                                   y=round(output_box.y - y),
                                                   width=output_box.width,
                                                   height=output_box.height))

    def view_map(self, view: View):
        logger.debug(f'Map {view}')
        if view.kind == WindowKind.X11_UNMANAGED:
            geo = view.geometry()
            x11_surface = view.x11_surface
            view.place(x11_surface.x, x11_surface.y, geo.width, geo.height)
            self.focus(view)
            return
        self._view_set_position(view)
        self.focus(view)

    def view_unmap(self, view: View):
        logger.debug(f'Unmap {view}')
        if view.wlr_surface == self._input_manager.focused_surface:
            self._input_manager.maybe_clear_keyboard_focus(view.wlr_surface)
        if next_view := next((v for v in reversed(self._views) if v != view and v.is_mapped), None):
            self.focus(next_view)

    def view_destroy(self, view: View):
        logger.debug(f'Destroy view {view}')
        self._views.remove(view)
        #if not self._is_quitting and self._app is not None and not self._app.poll():
        #     self.quit()

    def _window_by_surface(self, wlr_surface: Surface) -> Window | None:
        surface: XdgSurface | XWaylandSurface | None = None
        if (surface :=  XdgSurface.try_from_surface(wlr_surface)) is None:
            if _XWAYLAND_AVAILABLE:
                surface = XWaylandSurface.try_from_wlr_surface(wlr_surface)
        return cast(Window, surface.data) if surface else None

    def focus(self, window: Window):
        if not window.is_mapped:
            logger.debug('Attempt to focus an unmapped window')
            return
        wlr_surface = window.wlr_surface
        # "is_mapped" implies that a wlr_surface exists
        assert wlr_surface
        seat = self._input_manager.seat
        if not seat:
            return
        if self.exclusive_layer and self.exclusive_layer != window:
            return
        prev_surface = seat.keyboard_state.focused_surface
        if wlr_surface == prev_surface:
            return
        kb = seat.get_keyboard()
        if prev_surface:
            self._input_manager.maybe_clear_keyboard_focus(prev_surface)
            prev_win = self._window_by_surface(prev_surface)
            if prev_win and prev_win.kind != WindowKind.LAYER:
                prev_view = cast(View, prev_win)
                if prev_view.is_fullscreen:
                    prev_view.fullscreen(False)
                    prev_view.was_fullscreen = True
                prev_view.activated = False
                if prev_view.kind != WindowKind.X11_UNMANAGED and window.kind != WindowKind.X11_UNMANAGED:
                    dim = self._config.dim and not prev_win.is_transient_for(window)
                    prev_view.dim(dim)
                if not self._config.full_ftm:
                    prev_view.ftm_handle = None
        if kb:
            seat.keyboard_notify_enter(wlr_surface, kb)
        if scene_tree := window.scene_tree:
            scene_tree.node.raise_to_top()
        if window.kind != WindowKind.LAYER:
            view = cast(View, window)
            views = self._views[:]
            views.remove(view)
            views.append(view)
            self._views = views
            view.activated = True
            view.dim(False)
            if not view.is_xdg:
                view.x11_surface.restack(None, _XCB_STACK_MODE_ABOVE)
            if self._ft_manager and view.ftm_handle is None:
                view.ftm_handle = self._ft_manager.create_handle()
            if view.was_fullscreen:
                view.fullscreen(True)

    def _on_xwayland_ready(self, _: Any):
        logger.debug('Event: XWayland ready_event')
        assert self._xwayland
        seat = self._input_manager.seat
        assert seat
        self._xwayland.set_seat(seat)
        cursor_theme = self._config.cursor_theme
        xcursor_manager = self._input_manager.xcursor_manager
        if (xcursor := xcursor_manager.get_xcursor(cursor_theme)) is None:
            logger.warn(f'XWayland: No XCursor found for cursor theme "{cursor_theme}"')
            return
        if (image := next(xcursor.images, None)) is None:
            logger.warn(f'XWayland: No images found for cursor theme "{cursor_theme}"')
            return
        img_ptr = image._ptr
        self._xwayland.set_cursor(img_ptr.buffer, img_ptr.width * 4, img_ptr.width,
                                  img_ptr.height, img_ptr.hotspot_x, img_ptr.hotspot_y)

    def _on_output_new(self, output: Output):
        logger.debug(f'New output: name="{output.name}", description="{output.description}"')
        suggested_screen = self._config.screen
        if suggested_screen and output.name != suggested_screen:
            logger.debug(f'Output is ignored. Does not match "{suggested_screen}"')
            return
        output.init_render(self._allocator, self._renderer)
        state = OutputState()
        state.set_enabled(True)
        if output.current_mode is None:
            state.set_mode(output.preferred_mode())
        commit_succeed = output.commit(state)
        state.finish()
        if not commit_succeed:
            return
        if (layout_output := self.output_layout.add_auto(output)) is None:
            return
        scene_output = SceneOutput.create(self._scene, output)
        self._scene_output_layout.add_output(layout_output, scene_output)
        area = self.output_layout.get_box(output)
        view_area = self.output_layout.get_box(output)
        fs_rect = SceneRect(self.fullscreen_scene_tree, 0, 0, self._fullscreen_color)
        screen = Screen(server=self, output=output, fullscreen_rect=fs_rect,
                        area=area, view_area=view_area, scene_output=scene_output)
        logger.debug(f'New screen {screen}')
        self.screens.append(screen)
        if not self._input_manager.xcursor_manager.load(output.scale):
            logger.error(f'Cannot load cursors for {screen} for the provided scale "{output.scale}"')
        if not self.current_screen or output.name == suggested_screen:
            logger.debug(f'Set current screen to "{screen}"')
            self.current_screen = screen

    def _on_screen_destroy(self, screen: Screen):
        logger.debug(f'Destroy output {screen}')
        self.screens.remove(screen)
        if self.current_screen == screen:
            self.current_screen = next((screen for screen in self.screens if screen.is_enabled), None)
        if not self.current_screen and self._config.auto_terminate and not self._is_quitting:
            logger.info('All screens are gone, will terminate')
            self.quit()

    def _on_output_layout_change(self, _: Any):
        logger.debug('Event: output_layout.change_event')
        if not self.current_screen:
            return
        config = OutputConfigurationV1()
        output_layout = self.output_layout
        for screen in (screen for screen in self.screens if screen.is_enabled):
            output = screen.output
            output_box = output_layout.get_box(output)
            if not output_box:
                continue
            head = OutputConfigurationHeadV1.create(config, output)
            head.state.x = output_box.x
            head.state.y = output_box.y
            screen.area = output_box
            screen.view_area = Box(x=output_box.x, y=output_box.y,
                                   width=output_box.width, height=output_box.height)
            screen.scene_output.set_position(output_box.x, output_box.y)
            screen.fullscreen_rect.node.set_position(output_box.x, output_box.y)
            screen.fullscreen_rect.set_size(*screen.size)
            screen.arrange_layers()
        self._output_manager.set_configuration(config)
        self.screens.sort(key=lambda s: (s.area.x, s.area.y))
        self._update_view_positions()

    def _update_view_positions(self):
        """\
        Updates all view positions.
        """
        set_position = self._view_set_position
        for view in (view for view in self._views if view.is_mapped):
            set_position(view)

    def _view_set_position(self, view: View, layout_box: Box | None = None):
        """\
        Positions the provided view in a maximized form or in the center
        of the provided dimensions.
        """
        if layout_box is None:
            layout_box = self.output_layout.get_box()
            if screen := self.current_screen:
                layout_box = screen.view_area if not view.is_fullscreen else screen.area
        x, y, width, height = layout_box.x, layout_box.y, layout_box.width, layout_box.height
        view_width, view_height = view.size()
        maximized = (self._config.ignore_size or not view.has_fixed_size()) and view.is_main \
                        or (width < view_width or height < view_height)
        if not maximized:
            x = (width - view_width) // 2
            y = (height - view_height) // 2
            width, height = view_width, view_height
        view.place(x, y, width, height, maximized=maximized)

    def _outputs_reconfigure(self, config: OutputConfigurationV1, apply: bool):
        """\
        This function is called every time the configuration of the outputs is
        about to change.

        :param apply: Indicates if the config should be applied (committed) or tested.
        """
        logger.debug(f'Event: output_manager reconfigure {"apply" if apply else "test"}')

        def output_configure(head: OutputConfigurationHeadV1, output_state: OutputState) -> bool:
            head.state.apply(output_state)
            fn = head.state.output.commit if apply else head.state.output.test
            return fn(output_state)

        output_state = OutputState()
        configure = partial(output_configure, output_state=output_state)
        if all(map(configure, config.heads)):
            config.send_succeeded()
        else:
            config.send_failed()
        config.destroy()

    def _on_xdg_activation(self, event: XdgActivationV1RequestActivateEvent):
        if not event.surface:
            return
        if window := self._window_by_surface(event.surface):
            self.focus(window)

    def _app_spawn(self, cmd: str | list[str]):
        """\
        Executes the main application.
        """
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        r, w = os.pipe()
        self._app = subprocess.Popen(cmd, pass_fds=(r, w))
        os.close(w)
        self._event_loop.add_fd(r, self._app_terminated, _WL_EVENT_HANGUP | _WL_EVENT_ERROR)

    def _app_terminated(self, fd: int, mask, _: Any):
        logger.debug('Terminated')
        os.close(fd)
        if _WL_EVENT_ERROR & mask == _WL_EVENT_ERROR:
            logger.debug('Client process closed by error')
            self._app_result = 1
        elif _WL_EVENT_HANGUP & mask == _WL_EVENT_HANGUP:
            logger.debug('Client process closed normally')
        self.quit()

    def _handle_signal(self, sig_num: int, _: Any) -> int:
        logger.debug('Handle signel')
        if sig_num in (signal.SIGINT, signal.SIGTERM):
            self.quit()
        return 0


def _logging_file() -> Path:
    """\
    Returns the absolute path to the logging file.
    """
    default_log_dir = '$XDG_DATA_HOME'
    if (tmp := os.path.expandvars(default_log_dir)) == default_log_dir:
        log_directory = Path('~/.local/share').expanduser()
    else:
        log_directory = Path(tmp)
    log_directory = log_directory / 'gabbia'
    if not log_directory.exists():
        log_directory.mkdir()
    return log_directory / 'gabbia.log'


def _logging_setup(level: int, level_wlr: int, log_wlr=False):
    """\
    Setup the (wlroots and our own) logging.
    """
    def init_logger(logger_: logging.Logger, logging_file: Path):
        logger_.setLevel(level)
        formatter = logging.Formatter('%(asctime)s | %(funcName)s():L%(lineno)d | %(message)s')
        file_handler = logging.handlers.RotatingFileHandler(logging_file,
                                                            maxBytes=2_000_000,
                                                            backupCount=5)
        file_handler.setFormatter(formatter)
        logger_.addHandler(file_handler)
    init_log = partial(init_logger, logging_file=_logging_file())
    init_log(logger)
    wlroots_log.log_init(level_wlr)
    if log_wlr:
        init_log(wlroots_log.logger)


def run(cmd: str | list[str], config: Config | None = None) -> int:
    """\
    Runs Gabbia.

    :param cmd: The command/application to run.
    :param config: The configuration. If ``None``, the default :class:`Config` will be used.
    """
    if config is None:
        config = Config()
    _logging_setup(level=config.log_level, level_wlr=config.log_level_wlr,
                   log_wlr=config.log_wlr)
    return Server(config).run(cmd)


@dataclass(slots=True, kw_only=True, frozen=True)
class InputConfig:
    """\
    Input configuration.

    Internal class which should keep the :class:`InputManager` configuration
    independent of the :class:`Server` config.
    """

    keyboard_layout: str | None = field(default_factory=partial(os.environ.get, 'XKB_DEFAULT_LAYOUT'))
    """\
    Specifies the default keyboard layout.

    Depends on the ``XKB_DEFAULT_LAYOUT`` environment variable or is undefined by default.
    """

    keyboard_options: str | None = field(default_factory=partial(os.environ.get, 'XKB_DEFAULT_OPTIONS'))
    """\
    Keyboard options.

    Depends on the ``XKB_DEFAULT_OPTIONS`` environment variable or is undefined by default.
    """

    keyboard_variant: str | None = field(default_factory=partial(os.environ.get, 'XKB_DEFAULT_VARIANT'))
    """\
    Keyboard variant.

    Depends on the ``XKB_DEFAULT_VARIANT`` environment variable or is undefined by default.
    """

    keyboard_rate: int = field(default_factory=lambda: int(os.environ.get('WLC_REPEAT_RATE', 25)))
    """\
    Keyboard rate.

    Depends on the ``WLC_REPEAT_RATE`` environment variable or uses ``25`` by default.
    """

    keyboard_delay: int = field(default_factory=lambda: int(os.environ.get('WLC_REPEAT_DELAY', 600)))
    """\
    Keyboard delay.

    Depends on the ``WLC_REPEAT_DELAY`` environment variable or uses ``600`` by default.
    """

    allow_vt_change: bool = _DEBUG
    """\
    Indicates if Gabbia should allow a switch to another virtual terminal.
    """

    cursor_size: int = field(default_factory=lambda: int(os.environ.get('XCURSOR_SIZE', 24)))
    """\
    The cursor size.

    Depends on the ``XCURSOR_SIZE`` environment variable or uses 24.
    """

    cursor_theme: str = field(default_factory=lambda: str(os.environ.get('XCURSOR_THEME', 'default')))
    """\
    The cursor theme.

    Depends on the ``XCURSOR_THEME`` environment variable or uses 'default'.
    """


@dataclass(slots=True, kw_only=True, frozen=True)
class Config(InputConfig):
    """\
    Configuration of Gabbia.

    All configuration options provide a valuable default, so it should
    be safe to run Gabbia with the default values.
    """

    screen: str = ''
    """\
    Indicates the screen Gabbia should utilize.

    Uses the first screen by default.
    """

    ftm: bool = True
    """\
    Indicates if the foreign toplevel management protocol should be supported.
    """

    full_ftm: bool = False
    """\
    Indicates if Gabbia should give access to the all views or to the
    currect, active view only. By default, it gives access to the active
    view, only.

    Set to ``True`` if you want to manage multiple applications via foreign
    toplevel management protocol.
    """

    fullscreen_color: str = _FULLSCREEN_COLOR
    """\
    Sets the color of the fullscreen background if a view does not cover the
    whole output.

    A hexadecimal value of 3, 6 or 8 characters. Although not enforced,
    it makes sense to use a non-transparent color.
    """

    dim: bool = True
    """\
    Indicates if the non-active view should be dimmed.
    """

    dim_color: str = _DIM_COLOR
    """\
    Sets the dimming color.

    A hexadecimal value of 3, 6 or 8 characters.
    """

    ignore_size: bool = False
    """\
    Indicates if size hints should be ignored.

    Can be used to ignore the preferred size of an application.
    """

    ssd: bool = True
    """\
    Indicates if server side decorations should be enabled.
    """

    auto_terminate: bool = True
    """\
    Indicates if Gabbia should be terminated if no applications (or screens) left.
    """

    default_wayland_socket: bool = False
    """\
    Indicates if Gabbia should use the default Wayland socket ``wayland-0``.

    If ``False`` (default), Gabbia tries to use ``wayland-1`` .. ``wayland-32``,
    otherwise ``wayland-0`` .. ``wayland-32``.
    """

    no_x: bool = False
    """\
    Indicates that XWayland should not be supported even if available.
    """

    log_level: int = logging.WARNING if not _DEBUG else logging.DEBUG
    """\
    Indicates the logging level.

    It's by default :data:`logging.WARNING`.
    """

    log_level_wlr: int = logging.WARNING if not _DEBUG else logging.DEBUG
    """\
    Indicates the wlroots logging level.

    It's by default :data:`logging.WARNING`.
    """

    log_wlr: bool = _DEBUG
    """\
    Indicates if wlroots logging should be enabled.
    """


def _make_parser() -> argparse.ArgumentParser:

    def log_level(s: str) -> int:
        if s.isdigit():
            return int(s)
        try:
            return logging.getLevelNamesMapping()[s.upper()]
        except AttributeError:  # Python < 3.11
            return logging.getLevelName(s.upper())

    default_cfg = Config()
    parser = argparse.ArgumentParser(prog='gabbia',
                                     description=f'Wayland kiosk version {__version__}',
                                     epilog='Use -- when you want to pass arguments to the command',
                                     allow_abbrev=False)
    parser.add_mutually_exclusive_group().add_argument('--version', help="Shows Gabbia's version",
                                                       action='version', version=f'Gabbia {__version__}')
    parser.add_argument('--csd', help='Enable client side decorations',
                        required=False, default=not default_cfg.ssd, action='store_true')
    parser.add_argument('--no-x', help='Disable XWayland',
                        required=False, default=default_cfg.no_x, action='store_true')
    parser.add_argument('--no-ftm', help='Disables the foreign toplevel management protocol',
                        required=False, default=not default_cfg.ftm, action='store_true')
    parser.add_argument('--full-ftm', help='Gives access to all views via the foreign toplevel management protocol',
                        required=False, default=default_cfg.full_ftm, action='store_true')
    parser.add_argument('--no-dim', help='Disables the dimming of inactive views', action='store_true',
                        required=False, default=not default_cfg.dim)
    parser.add_argument('--dim-color', help='Sets the dim color (hexadecimal value of 3, 6, or 8 characters',
                        required=False, default=default_cfg.dim_color)
    parser.add_argument('--fullscreen-color', help='Sets the color of the fullscreen rect (hexadecimal value of 3, 6, or 8 characters',
                        required=False, default=default_cfg.fullscreen_color)
    parser.add_argument('--default-wayland-socket', help='Tries to use socket wayland-0',
                        required=False, default=default_cfg.default_wayland_socket, action='store_true')
    parser.add_argument('--ignore-size', help='Ignore size hints from applications and enforce a maximized view',
                        required=False, default=False, action='store_true')
    parser.add_argument('--vt', help='Allow change to another virtual terminal',
                        required=False, default=default_cfg.allow_vt_change, action='store_true')
    parser.add_argument('--screen', help='Specifies the screen which should be used.',
                        required=False, default=default_cfg.screen)
    parser.add_argument('--cursor-theme', help='Cursor theme', required=False,
                        default=default_cfg.cursor_theme, type=str)
    parser.add_argument('--cursor-size', help='Cursor size', required=False,
                        default=default_cfg.cursor_size, type=int)
    parser.add_argument('--kb-layout', help='Keyboard layout', required=False,
                        default=default_cfg.keyboard_layout, type=str)
    parser.add_argument('--kb-opts', help='Keyboard options', required=False,
                        default=default_cfg.keyboard_options, type=str)
    parser.add_argument('--kb-variant', help='Keyboard variant', required=False,
                        default=default_cfg.keyboard_variant, type=str)
    parser.add_argument('--kb-rate', help='Keyboard rate', required=False,
                        default=default_cfg.keyboard_rate, type=int)
    parser.add_argument('--kb-delay', help='Keyboard delay', required=False,
                        default=default_cfg.keyboard_delay, type=int)
    parser.add_argument('--log-level', help='Logging level', required=False,
                        default=default_cfg.log_level, type=log_level)
    parser.add_argument('--log-level-wlr', help='Logging level of wlroots', required=False,
                        default=default_cfg.log_level_wlr, type=log_level)
    parser.add_argument('--disable-wlr-log', help='Disables wlroots logging', required=False,
                        default=False, action='store_true')
    parser.add_argument('cmd', help='The command to run', nargs='+')
    return parser


def _parse_config(args=None) -> tuple[Config, str]:
    parser = _make_parser()
    try:
        args = parser.parse_args(args)
    except SystemExit as ex:
        parser.usage = argparse.SUPPRESS
        if ex.code != 0:
            parser.print_help()
        raise
    config = Config(default_wayland_socket=args.default_wayland_socket,
                    screen=args.screen, ssd=not args.csd,
                    allow_vt_change=args.vt, no_x=args.no_x,
                    cursor_theme=args.cursor_theme, cursor_size=args.cursor_size,
                    keyboard_rate=args.kb_rate, keyboard_delay=args.kb_delay,
                    keyboard_layout=args.kb_layout, keyboard_options=args.kb_opts,
                    keyboard_variant=args.kb_variant, log_level=args.log_level,
                    log_level_wlr=args.log_level_wlr, log_wlr=not args.disable_wlr_log,
                    ignore_size=args.ignore_size, ftm=not args.no_ftm,
                    full_ftm=args.full_ftm, dim=not args.no_dim,
                    dim_color=args.dim_color,)
    return config, args.cmd


def main():
    """\
    Runs Gabbia from the command line.
    """
    config, cmd = _parse_config()
    try:
        res = run(cmd, config)
    except OSError as ex:
        msg = f'Failed to spawn client "{cmd[0] if len(cmd) == 1 else cmd}": {ex}'
        logger.error(msg)
        print(msg, file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        msg = str(ex)
        logger.error(msg)
        print(msg, file=sys.stderr)
        sys.exit(1)
    sys.exit(res)


if __name__ == '__main__':
    main()
