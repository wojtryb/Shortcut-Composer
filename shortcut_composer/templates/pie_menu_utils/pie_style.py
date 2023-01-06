from dataclasses import dataclass
from PyQt5.QtGui import QColor


@dataclass
class PieStyle:
    pie_radius: int
    icon_radius: int
    area_color: QColor

    icon_color: QColor = QColor(75, 75, 75, 255)
    border_color: QColor = QColor(55, 55, 55, 255)
    active_color: QColor = QColor(100, 150, 230, 255)

    def __post_init__(self):
        self.widget_radius = self.pie_radius + self.icon_radius
        self.border_thickness = round(self.icon_radius*0.1)
        self.area_thickness = round(self.pie_radius*0.4)
