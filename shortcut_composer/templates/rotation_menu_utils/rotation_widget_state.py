# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from dataclasses import dataclass
from collections import defaultdict

from composer_utils import AnimationProgress


class Zone(Enum):
    DEADZONE = 0
    DISCRETE_ZONE = 1
    CONTIGUOUS_ZONE = 2


@dataclass
class WidgetState:
    selected_angle: int = 0
    selected_zone: Zone = Zone.DEADZONE

    def __post_init__(self):
        self.animations_in_progress = defaultdict(lambda: AnimationProgress())

    def reset(self):
        self.selected_angle = 0
        self.selected_zone = Zone.DEADZONE
        self.animations_in_progress.clear()

    def tick_animations(self):
        current_animation = self.animations_in_progress[self.selected_angle]
        if self.selected_zone == Zone.DISCRETE_ZONE:
            current_animation.up()

        for animation in self.animations_in_progress.values():
            if animation != current_animation:
                animation.down()
