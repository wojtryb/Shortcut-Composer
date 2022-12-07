from typing import List, TypeVar, Generic
import math

from PyQt5.QtGui import QColor

from shortcut_composer_config import (
    SHORT_VS_LONG_PRESS_TIME,
    ICON_RADIUS_PX,
    PIE_RADIUS_PX,
)
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita import Krita
from .pie_menu_utils import (
    PieWidget,
    LabelHolder,
    PieStyle,
    Label,
    AngleIterator
)

T = TypeVar('T')


class PieMenu(PluginAction, Generic[T]):
    def __init__(
        self, *,
        name: str,
        controller: Controller,
        values: List[T],
        instructions: List[Instruction] = [],
        short_vs_long_press_time: float = SHORT_VS_LONG_PRESS_TIME,
        pie_radius: int = PIE_RADIUS_PX,
        icon_radius: int = ICON_RADIUS_PX,
        area_color: QColor = QColor(55, 55, 55, 200),
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self._controller = controller
        self._style = PieStyle(
            pie_radius=pie_radius,
            icon_radius=icon_radius,
            area_color=area_color,
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

    def _create_labels(self, values: List[T]) -> LabelHolder:
        labels = LabelHolder()
        iterator = AngleIterator(
            center_distance=self._style.widget_radius,
            radius=self._style.pie_radius,
            amount=len(values)
        )
        for value, (angle, point) in zip(values, iterator):
            labels[angle] = Label(
                center=point,
                value=value,
                display_value=self._controller.get_label(value),
                style=self._style
            )
        return labels
