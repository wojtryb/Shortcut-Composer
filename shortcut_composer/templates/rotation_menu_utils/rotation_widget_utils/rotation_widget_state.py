# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from dataclasses import dataclass
from collections import defaultdict

from composer_utils import AnimationProgress


class Zone(Enum):
    """Zones in the widget."""

    DEADZONE = 0
    """Zone in which angle is not red."""
    INTERVALLIC_ZONE = 1
    """Zone in which angles are being red with intervals."""
    PRECISE_ZONE = 2
    """Zone in which angles are being red precisely."""


@dataclass
class WidgetState:
    """Represents current state of the widget."""

    selected_angle: int = 0
    selected_zone: Zone = Zone.DEADZONE

    def __post_init__(self) -> None:
        self.animations_in_progress = defaultdict(lambda: AnimationProgress())
        """State of animations for each intervallic pie."""

    def reset(self) -> None:
        """Reset the state to starting value."""
        self.selected_angle = 0
        self.selected_zone = Zone.DEADZONE
        self.animations_in_progress.clear()

    def tick_animations(self) -> None:
        """Update animations of intervallic pies."""
        current_animation = self.animations_in_progress[self.selected_angle]
        if self.selected_zone == Zone.INTERVALLIC_ZONE:
            current_animation.up()

        for animation in self.animations_in_progress.values():
            if animation != current_animation:
                animation.down()
