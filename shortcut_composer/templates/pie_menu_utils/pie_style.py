from dataclasses import dataclass
from PyQt5.QtGui import QColor


@dataclass
class PieStyle:
    pie_radius: int
    icon_radius: int
    widget_radius: int
    border_thickness: int
    area_thickness: int
    color: QColor = QColor(55, 55, 55, 230)
    border_color: QColor = QColor(55, 55, 55, 255)
