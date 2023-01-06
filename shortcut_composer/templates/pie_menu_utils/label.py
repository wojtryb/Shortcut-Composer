from typing import Union, Any

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPoint

from .pie_style import PieStyle
from dataclasses import dataclass


@dataclass
class Label:
    center: QPoint
    value: Any
    style: PieStyle
    display_value: Union[str, QPixmap]
