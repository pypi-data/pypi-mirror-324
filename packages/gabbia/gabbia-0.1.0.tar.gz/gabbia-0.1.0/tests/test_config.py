#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright (c) 2024 - 2025 -- Lars Heuer
#
import gabbia


def test_default_config():
    cfg = gabbia.Config()
    assert cfg.ssd
    if gabbia._DEBUG:
        assert cfg.auto_terminate
        assert cfg.allow_vt_change
    else:
        assert cfg.auto_terminate
        assert not cfg.allow_vt_change


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
