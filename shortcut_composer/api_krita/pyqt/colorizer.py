from PyQt5.QtGui import QColor
from ..enums import BlendingMode
from typing import Union


class Colorizer(QColor):

    def __init__(self, value: Union[int, BlendingMode]): ...

    def __new__(cls, value: Union[int, BlendingMode]) -> QColor:
        if isinstance(value, int):
            return cls.percentage(value)
        elif isinstance(value, BlendingMode):
            return cls.blending_mode(value)

    @staticmethod
    def percentage(percent: int):
        if percent == 100:
            return QColor(50, 150, 50)
        if percent >= 80:
            return QColor(100, 255, 100)
        if percent >= 30:
            return QColor(255, 255, 100)
        return QColor(150, 50, 50)

    BLENDING_MODES_MAP = {
        BlendingMode.NORMAL: QColor(255, 255, 255),
        BlendingMode.OVERLAY: QColor(100, 255, 100),
        BlendingMode.ADD: QColor(255, 255, 100),
    }

    @classmethod
    def blending_mode(cls, mode: BlendingMode):
        return cls.BLENDING_MODES_MAP.get(mode, QColor(220, 220, 220))
