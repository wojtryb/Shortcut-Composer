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
        icons: list,
        background_color: Optional[QColor],
        active_color: QColor,
    ) -> None:
        self._icons = icons
        self._base_size = Krita.screen_size/2560

        self.pie_radius_scale = pie_radius_scale
        self.icon_radius_scale = icon_radius_scale
        self.background_color = self._pick_background_color(background_color)
        self.active_color = active_color
        self.active_color_dark = QColor(
            round(active_color.red()*0.8),
            round(active_color.green()*0.8),
            round(active_color.blue()*0.8))

        self.pie_radius: int = round(
            165 * self._base_size
            * self.pie_radius_scale
            * Config.PIE_GLOBAL_SCALE.read())
        self.widget_radius = self.pie_radius + self.base_icon_radius

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
            255)

        self.font_multiplier = self.SYSTEM_FONT_SIZE[platform.system()]

    @property
    def base_icon_radius(self) -> int:
        return round(
            50 * self._base_size
            * self.icon_radius_scale
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    @property
    def max_icon_radius(self) -> int:
        if not self._icons:
            return 1
        return round(self.pie_radius * math.pi / len(self._icons))

    @property
    def icon_radius(self) -> int:
        """Icons radius depend on settings, but they have to fit in the pie."""
        return min(self.base_icon_radius, self.max_icon_radius)

    @property
    def deadzone_radius(self) -> float:
        """Deadzone can be configured, but when pie is empty, becomes inf."""
        if not self._icons:
            return float("inf")
        return (
            40 * self._base_size
            * Config.PIE_DEADZONE_GLOBAL_SCALE.read())

    def _pick_background_color(self, color: Optional[QColor]) -> QColor:
        """Default background color depends on the app theme lightness."""
        if color is not None:
            return color
        if Krita.is_light_theme_active:
            return QColor(210, 210, 210, 190)
        return QColor(75, 75, 75, 190)

    SYSTEM_FONT_SIZE = {
        "Linux": 0.175,
        "Windows": 0.11,
        "Darwin": 0.265,
        "": 0.125,
    }
    """Scale to fix different font sizes each OS.."""
