# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import math
import platform
from typing import TYPE_CHECKING

from PyQt5.QtGui import QColor

from api_krita import Krita
from composer_utils import Config

if TYPE_CHECKING:
    from .pie_config import PieConfig


class PieStyle:
    """
    Holds and calculates configuration of displayed elements.

    Style elements are calculated based on passed local config and
    imported global config.

    They are also affected by length of passed items list which size can
    change over time.
    """

    def __init__(
        self,
        pie_config: 'PieConfig',
        items: list,
    ) -> None:
        self._items = items
        self._base_size = Krita.screen_size/2560
        self._pie_config = pie_config

    @property
    def _pie_radius_scale(self) -> float:
        """Local scale of pie selected by user."""
        return self._pie_config.PIE_RADIUS_SCALE.read()

    @property
    def _icon_radius_scale(self) -> float:
        """Local scale of pie child selected by user."""
        return self._pie_config.ICON_RADIUS_SCALE.read()

    @property
    def pie_radius(self) -> int:
        """Radius in pixels at which icon centers are located."""
        return round(
            165 * self._base_size
            * self._pie_radius_scale
            * Config.PIE_GLOBAL_SCALE.read())

    @property
    def _base_icon_radius(self) -> int:
        """Radius of icons in pixels. Not affected by items amount."""
        return round(
            50 * self._base_size
            * self._icon_radius_scale
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    @property
    def unscaled_icon_radius(self) -> int:
        """Radius of icons in pixels. Ignores local scale and items amount."""
        return round(
            50 * self._base_size
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    @property
    def _max_icon_radius(self) -> int:
        """Max icon radius in pixels according to items amount."""
        if not self._items:
            return 1
        return round(self.pie_radius * math.pi / len(self._items))

    @property
    def icon_radius(self) -> int:
        """Icons radius depend on settings, but they have to fit in the pie."""
        return min(self._base_icon_radius, self._max_icon_radius)

    @property
    def deadzone_radius(self) -> float:
        """Deadzone can be configured, but when pie is empty, becomes inf."""
        if not self._items:
            return float("inf")
        return self.accept_button_radius

    @property
    def widget_radius(self) -> int:
        """Radius of the entire widget, including base and the icons."""
        return self.pie_radius + self._base_icon_radius

    @property
    def border_thickness(self):
        """Thickness of border around icons."""
        return round(self.icon_radius*0.12)

    @property
    def unscaled_border_thickness(self):
        """Thickness of border of the pie."""
        return round(self.unscaled_icon_radius*0.12)

    @property
    def area_thickness(self):
        """Thickness of the base area of pie menu."""
        return round(self.pie_radius*0.4)

    @property
    def inner_edge_radius(self):
        """Radius at which the base area starts."""
        return self.pie_radius - self.area_thickness

    @property
    def no_border_radius(self):
        """Radius at which pie decoration border starts."""
        return self.pie_radius - self.border_thickness//2

    @property
    def setting_button_radius(self) -> int:
        """Radius of the button which activates edit mode."""
        return round(30 * self._base_size)

    @property
    def accept_button_radius(self) -> int:
        """Radius of the button which applies the changes from edit mode."""
        return round(
            40 * self._base_size
            * Config.PIE_DEADZONE_GLOBAL_SCALE.read())

    @property
    def active_color(self) -> QColor:
        """
        Color of highlight, when label is active.

        If custom one is not specified, use the default one.
        """
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return self._pie_config.ACTIVE_COLOR.read()
        else:
            return Config.default_active_color

    @property
    def background_color(self) -> QColor:
        """
        Color of pie background area.

        If custom one is not specified, use the default one.
        Opacity is stored in a separate field in <0-100> range
        """
        if not self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return Config.default_background_color

        background_color = self._pie_config.BACKGROUND_COLOR.read()
        opacity = self._pie_config.PIE_OPACITY.read() * 255 / 100
        background_color.setAlpha(round(opacity))
        return background_color

    @property
    def active_color_dark(self):
        """Color variation of active element."""
        return QColor(
            round(self.active_color.red()*0.8),
            round(self.active_color.green()*0.8),
            round(self.active_color.blue()*0.8))

    @property
    def border_color(self):
        """Color of icon borders."""
        return QColor(
            min(self.background_color.red()+15, 255),
            min(self.background_color.green()+15, 255),
            min(self.background_color.blue()+15, 255),
            255)

    @property
    def font_multiplier(self):
        """Multiplier to apply to the font depending on the used OS."""
        return self.SYSTEM_FONT_SIZE[platform.system()]

    SYSTEM_FONT_SIZE = {
        "Linux": 0.175,
        "Windows": 0.11,
        "Darwin": 0.265,
        "": 0.125}
    """Scale to fix different font sizes each OS."""
