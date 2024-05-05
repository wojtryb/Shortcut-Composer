# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import defaultdict
from enum import Enum

from PyQt5.QtGui import QColor

from api_krita import Krita
from api_krita.enums import BlendingMode


class Color(Enum):
    """Named custom colors."""

    WHITE = QColor(248, 248, 248)
    LIGHT_GRAY = QColor(170, 170, 170)
    DARK_GRAY = QColor(90, 90, 90)
    BLACK = QColor(0, 0, 0)
    YELLOW = QColor(253, 214, 56)
    RED = QColor(245, 49, 116)
    ORANGE = QColor(236, 109, 39)
    GREEN = QColor(169, 224, 69)
    DARK_GREEN = QColor(119, 184, 55)
    BLUE = QColor(110, 217, 224)
    DARK_BLUE = QColor(42, 160, 251)
    VERY_DARK_BLUE = QColor(22, 130, 221)
    VIOLET = QColor(173, 133, 251)


class LabelTextColorizer(QColor):
    """Functions that return a color associated with value of property."""

    @staticmethod
    def action() -> QColor:
        """Return a QColor associated with action."""
        if Krita.is_light_theme_active:
            return Color.BLACK.value
        return Color.WHITE.value

    @classmethod
    def blending_mode(cls, mode: BlendingMode) -> QColor:
        """Return a QColor associated with blending mode."""
        if Krita.is_light_theme_active:
            return cls.BLENDING_MODES_LIGHT[mode].value
        return cls.BLENDING_MODES_DARK[mode].value

    @classmethod
    def percentage(cls, percent: int) -> QColor:
        """Return a QColor associated with percentage value."""
        return cls._percentage(percent).value

    @staticmethod
    def _percentage(percent: int) -> Color:
        """Mapping of percentage values to custom colors."""
        if Krita.is_light_theme_active:
            if percent >= 100:
                return Color.DARK_GREEN
            if percent >= 80:
                return Color.GREEN
            if percent >= 50:
                return Color.BLACK
            if percent > 25:
                return Color.DARK_GRAY
            if percent > 10:
                return Color.ORANGE
            return Color.RED
        else:
            if percent >= 100:
                return Color.DARK_GREEN
            if percent >= 80:
                return Color.GREEN
            if percent >= 50:
                return Color.WHITE
            if percent > 25:
                return Color.LIGHT_GRAY
            if percent > 10:
                return Color.YELLOW
            return Color.RED

    BLENDING_MODES_DARK = defaultdict(lambda: Color.LIGHT_GRAY, {
        BlendingMode.NORMAL: Color.WHITE,
        BlendingMode.ERASE: Color.VIOLET,
        BlendingMode.OVERLAY: Color.RED,
        BlendingMode.SCREEN: Color.GREEN,
        BlendingMode.COLOR: Color.YELLOW,
        BlendingMode.ADD: Color.DARK_BLUE,
        BlendingMode.MULTIPLY: Color.BLUE,
    })
    """Mapping of blending modes to custom colors in dark theme."""
    BLENDING_MODES_LIGHT = defaultdict(lambda: Color.DARK_GRAY, {
        BlendingMode.NORMAL: Color.BLACK,
        BlendingMode.ERASE: Color.VIOLET,
        BlendingMode.OVERLAY: Color.RED,
        BlendingMode.SCREEN: Color.ORANGE,
        BlendingMode.COLOR: Color.VIOLET,
        BlendingMode.ADD: Color.DARK_BLUE,
        BlendingMode.MULTIPLY: Color.VERY_DARK_BLUE,
    })
    """Mapping of blending modes to custom colors in light theme."""
