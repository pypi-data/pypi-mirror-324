#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright (c) 2024 - 2025 -- Lars Heuer
#
import pytest
from gabbia import _rgba

_BLACK = (.0, .0, .0, 1.)

_WHITE = (1., 1., 1., 1.)


@pytest.mark.parametrize('color, expected',
                         [('#000000', _BLACK),
                          ('#000', _BLACK),
                          ('000', _BLACK),
                          ('fff', _WHITE),
                          ('#fff', _WHITE),
                          ('#ffffffff', _WHITE),
                          ('#ffffff00', (1., 1., 1., 0.)),
                          ('#000000cc', (0., 0., 0., .8)),
                          ])
def test_rgba(color, expected):
    assert expected == _rgba(color)


@pytest.mark.parametrize('color',
                         ['#00',
                          'ff',
                          'ffff',
                          '#0000'
                          ])
def test_invalid_rgba(color):
    with pytest.raises(ValueError):
        _rgba(color)


if __name__ == '__main__':
    pytest.main([__file__])
