# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import platform
from typing import Callable

from PyQt5.QtGui import QColor


class LabelWidgetStyle:
    """
    Holds and calculates configuration of displayed elements.

    Style elements are calculated based on passed local config and
    imported global config.

    They are also affected by length of passed items list which size can
    change over time.
    """

    def __init__(
        self,
        icon_radius_callback: Callable[[], int],
        border_thickness_callback: Callable[[], int],
        active_color_callback: Callable[[], QColor],
        background_color_callback: Callable[[], QColor],
    ) -> None:
        self._icon_radius_callback = icon_radius_callback
        self._border_thickness_callback = border_thickness_callback
        self._active_color_callback = active_color_callback
        self._background_color_callback = background_color_callback

    @property
    def icon_radius(self) -> int:
        return self._icon_radius_callback()

    @property
    def border_thickness(self) -> int:
        return self._border_thickness_callback()

    @property
    def active_color(self) -> QColor:
        return self._active_color_callback()

    @property
    def background_color(self) -> QColor:
        return self._background_color_callback()

    @property
    def active_color_dark(self) -> QColor:
        """Color variation of active element."""
        return QColor(
            round(self.active_color.red()*0.8),
            round(self.active_color.green()*0.8),
            round(self.active_color.blue()*0.8))

    @property
    def border_color(self) -> QColor:
        """Color of icon borders."""
        return QColor(
            min(self.background_color.red()+15, 255),
            min(self.background_color.green()+15, 255),
            min(self.background_color.blue()+15, 255))

    @property
    def font_multiplier(self) -> float:
        """Multiplier to apply to the font depending on the used OS."""
        return self.SYSTEM_FONT_SIZE[platform.system()]

    SYSTEM_FONT_SIZE = {
        "Linux": 0.175,
        "Windows": 0.11,
        "Darwin": 0.265,
        "": 0.125}
    """Scale to fix different font sizes each OS."""
