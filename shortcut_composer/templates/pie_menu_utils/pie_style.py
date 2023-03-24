# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import math
import platform
from typing import Optional, Callable, List
from copy import copy

from PyQt5.QtGui import QColor

from api_krita import Krita
from composer_utils import Config
from config_system import Field


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
        pie_radius_scale: Field[float],
        icon_radius_scale: Field[float],
        background_color: Optional[QColor],
        active_color: QColor,
        items: list,
    ) -> None:
        self._items = items
        self._base_size = Krita.screen_size/2560

        self._pie_radius_scale = pie_radius_scale
        self._icon_radius_scale = icon_radius_scale
        self._background_color = background_color
        self.active_color = active_color

        self._pie_radius_scale.register_callback(self._notice_change)
        self._icon_radius_scale.register_callback(self._notice_change)
        self._on_change_callbacks: List[Callable[[], None]] = []

    def _notice_change(self):
        for callback in self._on_change_callbacks:
            callback()

    @property
    def pie_radius_scale(self):
        return self._pie_radius_scale.read()

    @property
    def icon_radius_scale(self):
        return self._icon_radius_scale.read()

    def register_callback(self, callback: Callable[[], None]):
        self._on_change_callbacks.append(callback)

    @property
    def pie_radius(self) -> int:
        return round(
            165 * self._base_size
            * self.pie_radius_scale
            * Config.PIE_GLOBAL_SCALE.read())

    @property
    def base_icon_radius(self) -> int:
        return round(
            50 * self._base_size
            * self.icon_radius_scale
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    @property
    def max_icon_radius(self) -> int:
        if not self._items:
            return 1
        return round(self.pie_radius * math.pi / len(self._items))

    @property
    def icon_radius(self) -> int:
        """Icons radius depend on settings, but they have to fit in the pie."""
        return min(self.base_icon_radius, self.max_icon_radius)

    @property
    def deadzone_radius(self) -> float:
        """Deadzone can be configured, but when pie is empty, becomes inf."""
        if not self._items:
            return float("inf")
        return (
            40 * self._base_size
            * Config.PIE_DEADZONE_GLOBAL_SCALE.read())

    @property
    def widget_radius(self):
        return self.pie_radius + self.base_icon_radius

    @property
    def border_thickness(self):
        return round(self.pie_radius*0.02)

    @property
    def area_thickness(self):
        return round(self.pie_radius/self.pie_radius_scale*0.4)

    @property
    def inner_edge_radius(self):
        return self.pie_radius - self.area_thickness

    @property
    def no_border_radius(self):
        return self.pie_radius - self.border_thickness//2

    @property
    def setting_button_radius(self) -> int:
        return round(30 * self._base_size)

    @property
    def accept_button_radius(self) -> int:
        default_radius = self.setting_button_radius
        radius = self.deadzone_radius
        return int(radius) if radius != float("inf") else default_radius

    @property
    def background_color(self) -> QColor:
        """Default background color depends on the app theme lightness."""
        if self._background_color is not None:
            return self._background_color
        if Krita.is_light_theme_active:
            return QColor(210, 210, 210, 190)
        return QColor(75, 75, 75, 190)

    @property
    def active_color_dark(self):
        return QColor(
            round(self.active_color.red()*0.8),
            round(self.active_color.green()*0.8),
            round(self.active_color.blue()*0.8))

    @property
    def icon_color(self):
        color = copy(self.background_color)
        color.setAlpha(255)
        return color

    @property
    def border_color(self):
        return QColor(
            min(self.icon_color.red()+15, 255),
            min(self.icon_color.green()+15, 255),
            min(self.icon_color.blue()+15, 255),
            255)

    @property
    def font_multiplier(self):
        return self.SYSTEM_FONT_SIZE[platform.system()]

    SYSTEM_FONT_SIZE = {
        "Linux": 0.175,
        "Windows": 0.11,
        "Darwin": 0.265,
        "": 0.125,
    }
    """Scale to fix different font sizes each OS.."""
