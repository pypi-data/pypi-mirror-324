#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright (c) 2024 - 2025 -- Lars Heuer
#
"""\
See <https://github.com/flacjacket/pywlroots/issues/218>
"""
from gabbia import Box


def test_empty():
    box = Box(x=0, y=0, width=0, height=0)
    assert not box
    box = Box(x=0, y=0, width=1, height=0)
    assert not box
    box = Box(x=0, y=0, width=0, height=1)
    assert not box
    box = Box(x=0, y=0, width=1, height=1)
    assert box


def test_equal():
    box1 = Box(x=0, y=0, width=10, height=10)
    box2 = Box(x=0, y=0, width=10, height=10)
    assert box1 == box2
    box2 = Box(x=0, y=0, width=100, height=10)
    assert box1 != box2


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
