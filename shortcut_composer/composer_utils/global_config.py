# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QColor

from api_krita import Krita
from config_system import FieldGroup


class GlobalConfig(FieldGroup):
    """
    Configuration fields available in the plugin.

    Each field can:
    - return its default value
    - read current value from krita config file in correct type
    - write given value to krita config file

    Class inherits a method which resets all config files.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.SHORT_VS_LONG_PRESS_TIME = self.field(
            name="Short vs long press time",
            default=0.3)
        self.TRACKER_SENSITIVITY_SCALE = self.field(
            name="Tracker sensitivity scale",
            default=1.0)
        self.TRACKER_DEADZONE = self.field(
            name="Tracker deadzone",
            default=0)
        self.FPS_LIMIT = self.field(
            name="FPS limit",
            default=60)

        self.PIE_GLOBAL_SCALE = self.field(
            name="Pie global scale",
            default=1.0)
        self.PIE_ICON_GLOBAL_SCALE = self.field(
            name="Pie icon global scale",
            default=1.0)
        self.PIE_DEADZONE_GLOBAL_SCALE = self.field(
            name="Pie deadzone global scale",
            default=1.0)
        self.PIE_ANIMATION_TIME = self.field(
            name="Pie animation time",
            default=0.2)

        self.OVERRIDE_BACKGROUND_THEME_COLOR = self.field(
            name="Override background theme color",
            default=False)
        self.DEFAULT_BACKGROUND_COLOR = self.field(
            name="Global background color",
            default=Krita.get_main_color_from_theme())

        self.OVERRIDE_ACTIVE_THEME_COLOR = self.field(
            name="Override active theme color",
            default=True)
        self.DEFAULT_ACTIVE_COLOR = self.field(
            name="Global active color",
            default=QColor(100, 150, 230))

        self.DEFAULT_PIE_OPACITY = self.field(
            name="Global pie opacity",
            default=75)

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
