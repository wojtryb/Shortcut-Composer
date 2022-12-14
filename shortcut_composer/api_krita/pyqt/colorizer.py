from typing import Union
from enum import Enum

from PyQt5.QtGui import QColor

from ..enums import BlendingMode


class Color(Enum):

    ORANGE = QColor(236, 109, 39)
    LIGHT_GRAY = QColor(170, 170, 170)
    BLUE = QColor(110, 217, 224)
    GREEN = QColor(169, 224, 69)
    DARK_GREEN = QColor(119, 184, 55)
    RED = QColor(245, 49, 116)
    YELLOW = QColor(253, 214, 56)
    VIOLET = QColor(173, 133, 251)
    DARK_BLUE = QColor(42, 160, 251)
    WHITE = QColor(248, 248, 242)


class Colorizer(QColor):

    def __init__(self, value: Union[int, BlendingMode]): ...

    def __new__(cls, value: Union[int, BlendingMode]) -> QColor:
        if isinstance(value, int):
            return cls.percentage(value).value
        elif isinstance(value, BlendingMode):
            return cls.blending_mode(value).value

    @staticmethod
    def percentage(percent: int) -> Color:
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

    BLENDING_MODES_MAP = {
        BlendingMode.NORMAL: Color.WHITE,
        BlendingMode.OVERLAY: Color.RED,
        BlendingMode.SCREEN: Color.GREEN,
        BlendingMode.COLOR: Color.YELLOW,
        BlendingMode.ADD: Color.DARK_BLUE,
        BlendingMode.MULTIPLY: Color.BLUE,
    }

    @classmethod
    def blending_mode(cls, mode: BlendingMode) -> Color:
        return cls.BLENDING_MODES_MAP.get(mode, Color.LIGHT_GRAY)
