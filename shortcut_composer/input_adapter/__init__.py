# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module contains utilities that allow to connect custom actions to krita.

ActionManager (public) allows to use custom action interface of
ComplexAction (public) that supports:
- key pressing
- key releasing
- distinguishing between short and long key presses

It has no external dependencies, so that it can be copy-pasted to any
other krita plugin.
"""

from .action_manager import ActionManager
from .complex_action_interface import ComplexActionInterface

__all__ = ['ActionManager', 'ComplexActionInterface']
