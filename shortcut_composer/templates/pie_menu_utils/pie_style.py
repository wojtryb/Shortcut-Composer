from dataclasses import dataclass
from copy import copy
from PyQt5.QtGui import QColor

from api_krita import Krita
from shortcut_composer_config import PIE_DEADZONE_SCALE


@dataclass
class PieStyle:
    pie_radius_scale: float
    icon_radius_scale: float
    area_color: QColor
    active_color: QColor

    def __post_init__(self):
        base_size = Krita.screen_size/2560

        self.pie_radius = round(base_size * self.pie_radius_scale * 165)
        self.icon_radius = round(base_size * self.icon_radius_scale * 50)
        self.deadzone_radius: float = base_size * PIE_DEADZONE_SCALE * 40

        self.widget_radius = self.pie_radius + self.icon_radius

        self.border_thickness = round(self.icon_radius*0.06)
        self.area_thickness = round(self.pie_radius/self.pie_radius_scale*0.4)

        self.icon_color = copy(self.area_color)
        self.icon_color.setAlpha(255)

        self.border_color = QColor(
            max(self.icon_color.red()+15, 0),
            max(self.icon_color.green()+15, 0),
            max(self.icon_color.blue()+15, 0),
            255
        )

    def update_icon_radius(self, amount: int):
        if not amount:
            return
        max_icon_size = round(self.pie_radius * 3.1413 / amount)
        self.icon_radius = min(self.icon_radius, max_icon_size)
