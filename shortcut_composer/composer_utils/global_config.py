# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from config_system import FieldGroup
from PyQt5.QtGui import QColor
from api_krita import Krita


class GlobalConfig(FieldGroup):
    """
    Configuration fields available in the plugin.

    Each field can:
    - return its default value
    - read current value from krita config file in correct type
    - write given value to krita config file

    Class holds a staticmethod which resets all config files.

    VALUES configs are string representations of lists. They hold values
    to use in given action with elements separated with tabulators.
    These are needed to be further parsed using TagConfigValues or
    EnumConfigValues.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.SHORT_VS_LONG_PRESS_TIME = self.field(
            "Short vs long press time", 0.3)
        self.TRACKER_SENSITIVITY_SCALE = self.field(
            "Tracker sensitivity scale", 1.0)
        self.TRACKER_DEADZONE = self.field("Tracker deadzone", 0)
        self.FPS_LIMIT = self.field("FPS limit", 60)

        self.PIE_GLOBAL_SCALE = self.field("Pie global scale", 1.0)
        self.PIE_ICON_GLOBAL_SCALE = self.field("Pie icon global scale", 1.0)
        self.PIE_DEADZONE_GLOBAL_SCALE = self.field(
            "Pie deadzone global scale", 1.0)
        self.PIE_ANIMATION_TIME = self.field("Pie animation time", 0.2)

        self.OVERRIDE_BACKGROUND_THEME_COLOR = self.field(
            "Override background theme color", False)
        self.DEFAULT_BACKGROUND_COLOR = self.field(
            "Global bg color", Krita.get_main_color_from_theme())

        self.OVERRIDE_ACTIVE_THEME_COLOR = self.field(
            "Override active theme color", True)
        self.DEFAULT_ACTIVE_COLOR = self.field(
            "Global active color", QColor(100, 150, 230))

        self.DEFAULT_PIE_OPACITY = self.field("Global pie opacity", 75)

    def get_sleep_time(self) -> int:
        """Read sleep time from FPS_LIMIT config field."""
        fps_limit = self.FPS_LIMIT.read()
        return round(1000/fps_limit) if fps_limit else 1

    @property
    def default_background_color(self) -> QColor:
        """Color of pies, when the pie does not specify a custom one."""
        if self.OVERRIDE_BACKGROUND_THEME_COLOR.read():
            bg_color = self.DEFAULT_BACKGROUND_COLOR.read()
        else:
            bg_color = Krita.get_main_color_from_theme()
        opacity = self.DEFAULT_PIE_OPACITY.read() * 255 / 100
        bg_color.setAlpha(round(opacity))
        return bg_color

    @property
    def default_active_color(self) -> QColor:
        """Pie highlight color, when the pie does not specify a custom one."""
        if self.OVERRIDE_ACTIVE_THEME_COLOR.read():
            return self.DEFAULT_ACTIVE_COLOR.read()
        return Krita.get_active_color_from_theme()


Config = GlobalConfig("ShortcutComposer")
