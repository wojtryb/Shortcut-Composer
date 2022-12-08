from typing import Union, Any
from dataclasses import dataclass

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPoint

from api_krita.pyqt import Text
from .pie_style import PieStyle


@dataclass
class Label:
    center: QPoint
    angle: int
    value: Any
    style: PieStyle
    display_value: Union[Text, QPixmap]
