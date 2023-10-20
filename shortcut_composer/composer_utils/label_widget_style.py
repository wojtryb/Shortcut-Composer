# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import platform
from PyQt5.QtGui import QColor

from api_krita import Krita
from .global_config import Config


class LabelWidgetStyle:
    """
    Holds and calculates configuration of displayed elements.

    Style elements are calculated based on passed local config and
    imported global config.

    They are also affected by length of passed items list which size can
    change over time.
    """

    def __init__(self) -> None:
        self._base_size = Krita.screen_size/2560

        self.max_icon_radius = 100
        self.icon_radius_scale = 1.0
        self.active_color = QColor(0, 0, 0)
        self.background_color = QColor(0, 0, 0)

    @property
    def base_icon_radius(self) -> int:
        """Radius of icons in pixels. Not affected by items amount."""
        return round(
            50 * self._base_size
            * self.icon_radius_scale
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    @property
    def unscaled_icon_radius(self) -> int:
        """Radius of icons in pixels. Ignores local scale and items amount."""
        return round(
            50 * self._base_size
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    @property
    def icon_radius(self) -> int:
        """Icons radius depend on settings, but they have to fit in the pie."""
        return min(self.base_icon_radius, self.max_icon_radius)

    @property
    def border_thickness(self):
        """Thickness of border of the icons."""
        return round(self.unscaled_icon_radius*0.05)

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
