#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright (c) 2024 - 2025 -- Lars Heuer
#
import logging
import gabbia
from gabbia import _parse_config


def test_log_level_default():
    default_log_level = logging.DEBUG if gabbia._DEBUG else logging.WARNING
    config, cmd = _parse_config(['thunar'])
    assert default_log_level == config.log_level
    assert default_log_level == config.log_level_wlr
    assert ['thunar'] == cmd


def test_log_level_change():
    config, _ = _parse_config(['--log-level', 'info', 'thunar'])
    assert logging.INFO == config.log_level
    config, _ = _parse_config(['--log-level', 'eRRoR', 'thunar'])
    assert logging.ERROR == config.log_level


def test_disable_x11():
    config, _ = _parse_config(['--no-x', 'thunar'])
    assert config.no_x


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
