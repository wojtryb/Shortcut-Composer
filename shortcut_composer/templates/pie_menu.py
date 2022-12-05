from typing import List, TypeVar, Generic
import math

from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint

from shortcut_composer_config import (
    SHORT_VS_LONG_PRESS_TIME,
    ICON_RADIUS_PX,
    PIE_RADIUS_PX,
)
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita import Krita
from .pie_menu_utils import PieWidget, LabelHolder, PieStyle, Label

T = TypeVar('T')


class PieMenu(PluginAction, Generic[T]):
    def __init__(
        self, *,
        name: str,
        controller: Controller,
        values: List[T],
        instructions: List[Instruction] = [],
        short_vs_long_press_time: float = SHORT_VS_LONG_PRESS_TIME,
        pie_radius_px: int = PIE_RADIUS_PX,
        icon_radius_px: int = ICON_RADIUS_PX,
        color: QColor = QColor(55, 55, 55, 230),
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self._controller = controller
        self._style = PieStyle(
            pie_radius=pie_radius_px,
            icon_radius=icon_radius_px,
            widget_radius=pie_radius_px + icon_radius_px,
            border_thickness=round(icon_radius_px*0.1),
            area_thickness=round(pie_radius_px*0.4),
            color=color,
            border_color=QColor(55, 55, 55, 255),
        )
        self._labels = self._create_labels(values)
        self._widget = PieWidget(controller, self._labels, self._style)

    def on_key_press(self) -> None:
        self._controller.refresh()
        cursor = Krita.get_cursor()
        self.start = (cursor.x(), cursor.y())
        self._widget.move_center(*self.start)
        self._widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        cursor = Krita.get_cursor()
        angle = math.degrees(math.atan2(
            (-self.start[0] + cursor.x()),
            (self.start[1] - cursor.y())
        ))
        angle %= 360
        label = self._labels.closest(round(angle))
        self._controller.set_value(label.value)
        self._widget.hide()

    def _center_from_angle(self, angle: int, distance: int) -> QPoint:
        rad_angle = math.radians(angle)
        return QPoint(
            round(self._style.widget_radius + distance*math.sin(rad_angle)),
            round(self._style.widget_radius - distance*math.cos(rad_angle)),
        )

    def _create_labels(self, values: List[T]) -> LabelHolder:
        labels = LabelHolder()

        iterator = range(0, 360, round(360/len(values)))
        for value, angle in zip(values, iterator):
            distance = self._style.pie_radius
            label_center = self._center_from_angle(angle, distance)

            labels[angle] = Label(
                center=label_center,
                value=value,
                display_value=self._controller.get_label(value),
                style=self._style

            )
        return labels
