# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum


class DeadzoneStrategy(Enum):
    """
    Enumeration of actions that can be done on deadzone key release.

    Values are strings meant for being displayed in the UI.
    """
    DO_NOTHING = "Do nothing"
    """No action is needed."""
    PICK_TOP = "Pick top"
    """First label in list is activated."""
    PICK_PREVIOUS = "Pick previous"
    """Remembered label is activated."""


class RotationDeadzoneStrategy(Enum):
    """
    Enumeration of actions that can be done on deadzone of RotationMenu.

    Values are strings meant for being displayed in the UI.
    """
    KEEP_CHANGE = "Keep change"
    """Does nothing when moving into deadzone."""
    DISCARD_CHANGE = "Discard change"
    """Sets initial value when moving into deadzone."""
    SET_ZERO = "Set zero"
    """Sets 0 when inside the deadzone."""
