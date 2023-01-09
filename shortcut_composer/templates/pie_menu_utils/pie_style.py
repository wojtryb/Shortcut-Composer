# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import math
import platform
from typing import Optional
from dataclasses import dataclass
from copy import copy

from PyQt5.QtGui import QColor

from api_krita import Krita
from composer_utils import Config


@dataclass
class PieStyle:
    """
    Holds and calculates configuration of displayed elements.

    All style elements are calculated based on passed base colors and
    scale multipliers.

    Using adapt_to_item_amount() allows to modify the style to make it
    fit the given amount of labels.
    """

    def __init__(
        self,
        pie_radius_scale: float,
        icon_radius_scale: float,
        background_color: Optional[QColor],
        active_color: QColor,
    ) -> None:

        self.pie_radius_scale = pie_radius_scale
        self.icon_radius_scale = icon_radius_scale
        self.background_color = self._pick_background_color(background_color)
        self.active_color = active_color

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
            min(self.icon_color.red()+15, 255),
            min(self.icon_color.green()+15, 255),
            min(self.icon_color.blue()+15, 255),
            255
        )

        font_multiplier = self.SYSTEM_FONT_SIZE[platform.system()]
        self.font_size: int = round(self.icon_radius*font_multiplier)

    def adapt_to_item_amount(self, amount: int) -> None:
        """Modify the style to make it fit the given amount of labels."""
        if not amount:
            self.deadzone_radius = float("inf")
            return
        max_icon_size = round(self.pie_radius * math.pi / amount)
        self.icon_radius = min(self.icon_radius, max_icon_size)

    def _pick_background_color(self, color: Optional[QColor]) -> QColor:
        if color is not None:
            return color
        if Krita.is_light_theme_active:
            return QColor(210, 210, 210, 190)
        return QColor(75, 75, 75, 190)

    SYSTEM_FONT_SIZE = {
        "Linux": 0.40,
        "Windows": 0.25,
        "Darwin": 0.6,
        "": 0.25,
    }
