from dataclasses import dataclass
from copy import copy
from PyQt5.QtGui import QColor


@dataclass
class PieStyle:
    pie_radius: int
    icon_radius: int
    area_color: QColor
    active_color: QColor

    def __post_init__(self):
        self.widget_radius = self.pie_radius + self.icon_radius
        self.border_thickness = round(self.icon_radius*0.06)
        self.area_thickness = round(self.pie_radius*0.4)

        self.icon_color = copy(self.area_color)
        self.icon_color.setAlpha(255)

        self.border_color = QColor(
            max(self.icon_color.red()-15, 0),
            max(self.icon_color.green()-15, 0),
            max(self.icon_color.blue()-15, 0),
            255
        )
