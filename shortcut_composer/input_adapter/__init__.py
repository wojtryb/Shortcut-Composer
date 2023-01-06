# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module contains utilities that allow to connect custom actions to krita.

ActionManager (public) allows to use custom action interface of
ComplexAction (public) that supports key pressing, releasing and counting
time to differentiate short and long presses.

Custom interface is achieved by using ShortcutAdapters (private) - each
instance is responsible for finding right time to call methods of the
ctions.

Key pressing is achieved the usual way, by connecting a method to right
signal, but key releases require usage of EventFilter (private) common
for all actions.
"""

from .action_manager import ActionManager
from .complex_action import ComplexAction

__all__ = ['ActionManager', 'ComplexAction']
