# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
The only python file directly run by krita during plugin init phase.

Runs the file with extension by importing everything from it.

Appending this file location to python PATH allows to directly import
main packages instead of using relative imports.
"""
import sys
import os

sys.path.append(directory := os.path.dirname(__file__))

from .shortcut_composer import ShortcutComposer
from .api_krita import Krita
Krita.add_extension(ShortcutComposer)

sys.path.remove(directory)
