import math
from dataclasses import dataclass
from copy import copy

from PyQt5.QtGui import QColor

from api_krita import Krita
from shortcut_composer_config import (
    PIE_DEADZONE_GLOBAL_SCALE,
    ICON_RADIUS_GLOBAL_SCALE,
    PIE_RADIUS_GLOBAL_SCALE,
)


@dataclass
class PieStyle:

    pie_radius_scale: float
    icon_radius_scale: float
    background_color: QColor
    active_color: QColor

    def __post_init__(self):
        base_size = Krita.screen_size/2560

        self.pie_radius = round(
            165 * base_size
            * self.pie_radius_scale
            * ICON_RADIUS_GLOBAL_SCALE
        )
        self.icon_radius = round(
            50 * base_size
            * self.icon_radius_scale
            * PIE_RADIUS_GLOBAL_SCALE
        )
        self.deadzone_radius: float = (
            40 * base_size
            * PIE_DEADZONE_GLOBAL_SCALE
        )

        self.widget_radius = self.pie_radius + self.icon_radius

        self.border_thickness = round(self.pie_radius*0.02)
        self.area_thickness = round(self.pie_radius/self.pie_radius_scale*0.4)

        self.icon_color = copy(self.background_color)
        self.icon_color.setAlpha(255)

        self.border_color = QColor(
            max(self.icon_color.red()+15, 0),
            max(self.icon_color.green()+15, 0),
            max(self.icon_color.blue()+15, 0),
            255
        )

    def adapt_to_item_amount(self, amount: int) -> None:
        if not amount:
            self.deadzone_radius = float("inf")
            return
        max_icon_size = round(self.pie_radius * math.pi / amount)
        self.icon_radius = min(self.icon_radius, max_icon_size)
