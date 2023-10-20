# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import platform
from PyQt5.QtGui import QColor

# from api_krita import Krita


class LabelWidgetStyle:
    """
    Holds and calculates configuration of displayed elements.

    Style elements are calculated based on passed local config and
    imported global config.

    They are also affected by length of passed items list which size can
    change over time.
    """

    def __init__(self) -> None:
        self.icon_radius = 100
        self.border_thickness = 5
        self.active_color = QColor(0, 0, 0)
        self.background_color = QColor(0, 0, 0)

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
            min(self.background_color.blue()+15, 255))

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
