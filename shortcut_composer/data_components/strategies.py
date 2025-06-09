# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum


class PieDeadzoneStrategy(Enum):
    """
    Specifies actions that can be done on deadzone key release in Pie.

    Values are strings meant for being displayed in the UI.
    """
    DO_NOTHING = "Do nothing"
    """No action is needed."""
    PICK_TOP = "Pick top"
    """Label on the top is activated."""
    PICK_PREVIOUS = "Pick previous"
    """Previously selected label is activated."""


class RotationDeadzoneStrategy(Enum):
    """
    Specifies actions that can be done on deadzone of RotationSelector.

    Values are strings meant for being displayed in the UI.
    """
    KEEP_CHANGE = "Keep change"
    """Does nothing when moving into deadzone."""
    DISCARD_CHANGE = "Discard change"
    """Sets initial value when moving into deadzone."""
    SET_TO_ZERO = "Set to zero"
    """Sets 0 when inside the deadzone."""


class PickLayerStrategy(Enum):
    """
    Specifies what layers to pick when scrolling through layers.

    Values are strings meant for being displayed in the UI.
    """
    ALL = "Pick all"
    """Pick all the nodes in the stack (layers, groups, masks...)."""
    VISIBLE = "Visible"
    """Pick active node and all the nodes that are visible."""
    CURRENT_VISIBILITY = "Current visibility"
    """Pick all the nodes with the same visibility as the active node."""
    ANIMATED = "Animated"
    """Pick active node and all the nodes that have animation frames."""
    PINNED = "Pinned"
    """Pick active node and all the nodes that are pinned to timeline."""
