# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import math
import platform
from dataclasses import dataclass
from copy import copy

from PyQt5.QtGui import QColor

from composer_utils import Config
from api_krita import Krita


@dataclass
class PieStyle:
    """
    Holds and calculates configuration of displayed elements.

    All style elements are calculated based on passed base colors and
    scale multipliers.

    Using adapt_to_item_amount() allows to modify the style to make it
    fit the given amount of labels.
    """

    pie_radius_scale: float
    icon_radius_scale: float
    background_color: QColor
    active_color: QColor

    def __post_init__(self):
        base_size = Krita.screen_size/2560

        self.pie_radius = round(
            165 * base_size
            * self.pie_radius_scale
            * Config.PIE_GLOBAL_SCALE.read()
        )
        self.icon_radius = round(
            50 * base_size
            * self.icon_radius_scale
            * Config.PIE_ICON_GLOBAL_SCALE.read()
        )
        self.deadzone_radius: float = (
            40 * base_size
            * Config.PIE_DEADZONE_GLOBAL_SCALE.read()
        )
        self.widget_radius = self.pie_radius + self.icon_radius

        self.border_thickness = round(self.pie_radius*0.02)
        self.area_thickness = round(self.pie_radius/self.pie_radius_scale*0.4)

        self.inner_edge_radius = self.pie_radius - self.area_thickness
        self.no_border_radius = self.pie_radius - self.border_thickness//2

        self.icon_color = copy(self.background_color)
        self.icon_color.setAlpha(255)

        self.border_color = QColor(
            max(self.icon_color.red()+15, 0),
            max(self.icon_color.green()+15, 0),
            max(self.icon_color.blue()+15, 0),
            255
        )

        font_multiplier = self.SYSTEM_FONT_SIZE[platform.system()]
        self.font_size = round(self.icon_radius*font_multiplier)

    def adapt_to_item_amount(self, amount: int) -> None:
        """Modify the style to make it fit the given amount of labels."""
        if not amount:
            self.deadzone_radius = float("inf")
            return
        max_icon_size = round(self.pie_radius * math.pi / amount)
        self.icon_radius = min(self.icon_radius, max_icon_size)

    SYSTEM_FONT_SIZE = {
        "Linux": 0.45,
        "Windows": 0.25,
        "Darwin": 0.25,
        "": 0.25,
    }
