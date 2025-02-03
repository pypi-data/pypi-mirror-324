#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright (c) 2024 - 2025 -- Lars Heuer
#
"""
Configuration file for the Sphinx documentation builder.

https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import gabbia  # noqa: E402

project = 'Gabbia'
copyright = '2024 - 2025, Lars Heuer'
author = 'Lars Heuer'
version = gabbia.__version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'pywayland': ('https://pywayland.readthedocs.io/en/latest/', None)}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = '.rst'

html_theme = 'piccolo_theme'
html_theme_options = {
    'source_url': 'https://github.com/heuer/gabbia',
    'source_icon': 'github',
    'globaltoc_collapse': False
}

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('man/gabbia', 'gabbia', 'Gabbia - A Wayland kiosk', '', 1),
]
