# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from dataclasses import dataclass


class Zone(Enum):
    DEADZONE = 0
    DISCRETE_ZONE = 1
    CONTIGUOUS_ZONE = 2


@dataclass
class WidgetState:
    selected_angle: int = 0
    selected_zone: Zone = Zone.DEADZONE

    def reset(self):
        self.selected_angle = 0
        self.selected_zone = Zone.DEADZONE
