gabbia
======

Synopsis
--------

**gabbia** [*options*] application


Description
-----------

:program:`gabbia` is a Wayland kiosk.

It can be used to run a single application in maximized mode.


Command Line Options
--------------------

.. program:: gabbia


.. option:: --version

    Shows Gabbia's version and exit

.. option:: -h, --help

    Show a help message which lists all commands and exit


Keyboard Options
~~~~~~~~~~~~~~~~

.. option:: --kb-layout ALPHA_CODE

   Sets the keyboard layout. The layout should be determined by providing an alpha code

.. option:: --kb-opts OPTIONS

   Sets the keyboard options.

.. option:: --kb-variant VARIANT

    Sets the keyboard variant.

.. option:: --kb-rate RATE

    Sets the keyboard rate.

.. option:: --kb-delay DELAY

    Sets the keyboard delay.


Cursor Options
~~~~~~~~~~~~~~

.. option:: --cursor-theme CURSOR_THEME

    Sets the cursor theme.

.. option:: --cursor-size CURSOR_SIZE

    Sets the cursor size


Forgein toplevel management
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. option:: --no-ftm

   Disables support for the foreign toplevel management protocol

.. option:: --full-ftm

   Indicates that all toplevels should be available through the
   foreign toplevel management protocol. By default, only the
   current focused toplevel will be made available.


Dimming
~~~~~~~

.. option:: --no-dim

   Disables dimming of unfocused windows

.. option:: --dim-color COLOR

   Sets the dim color.
   The value must be a hexadecimal RGB(A) value with a length 3, 6, or 8
   characters. A hash sign at the beginning is optional.

   The dim color is ignored if --no-dim was provided.


Logging
~~~~~~~

.. option:: --log-level LOG_LEVEL

   Sets the logging level for Gabbia. Either a numerical value or the
   name of the log level.

.. option:: --log-level-wlr LOG_LEVEL

   Sets the log level of the wlroots logger.

.. option:: --disable-wlr-log

   Disables the wlroots logger.


Other Options
~~~~~~~~~~~~~~

.. option:: --csd

    Disables server side decorations (default) and enables client side decorations.

.. option:: --vt

   Enables switching to another terminal (disabled by default).

.. option:: --no-x

   Disables support for XWayland even if XWayland may be available.
   This limits Gabbia to run Wayland applications, only.

.. option:: --default-wayland-socket

   Tries to use "wayland-0" as socket name.

   By default, Gabbia avoids "wayland-0" and uses "wayland-1" or any higher
   value.

.. option:: --fullscreen-color COLOR

   Sets the color of the fullscreen background.

   If a fullscreen window does not fill the complete screen, the background
   color is used to hide other applications according to the XDG Shell protocol.

   The value must be a hexadecimal RGB(A) value with a length 3, 6, or 8
   characters. A hash sign at the beginning is optional.

   Although not enforced by Gabbia, it may make sense to use a non-tranparent
   color.


Environment
-----------

DISPLAY
~~~~~~~

    If run with XWayland support, Gabbia sets this environment variable
    to the XWayland server.


WAYLAND_DISPLAY
~~~~~~~~~~~~~~~

    This environment variable is set by Gabbia to the Wayland socket name.


XCURSOR_THEME
~~~~~~~~~~~~~

    Specifies the cursor theme.


XCURSOR_SIZE
~~~~~~~~~~~~

    Specifies the cursor size.


WLC_REPEAT_RATE
~~~~~~~~~~~~~~~

    Spefifies the keyboard repeat rate.


WLC_REPEAT_DELAY
~~~~~~~~~~~~~~~~

    Specifies the keyboard repeat delay.


XKB_DEFAULT_RULES, XKB_DEFAULT_LAYOUT, XKB_DEFAULT_VARIANT, XKB_DEFAULT_OPTIONS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Configures the xkb keyboard settings, see :manpage:`xkeyboard-config(7)`


Exit Status
-----------
:program:`gabbia` exits 0 on success, and 1 if an error occurs.


Examples
--------

.. code-block:: bash

    $ gabbia alacritty

Starts alacritty as maximized application.


.. code-block:: bash

    $ gabbia -- firefox https://gabbia.org/

Starts Firefox and opens the provided URL.


Internet Resources
------------------

    * Main website: https://gabbia.org/
    * Documentation: https://docs.gabbia.org/
    * Bug reports: https://github.com/heuer/gabbia/issues/


Licensing
---------

Gabbia is distributed under the MIT License. See the file "LICENSE" in
the source distribution for information on terms and conditions.

