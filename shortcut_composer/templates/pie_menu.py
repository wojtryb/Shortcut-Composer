from typing import List, TypeVar, Generic
import math

from PyQt5.QtGui import QColor

from shortcut_composer_config import (
    SHORT_VS_LONG_PRESS_TIME,
    PIE_ICON_RADIUS_PX,
    PIE_RADIUS_PX,
)
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita import Krita
from .pie_menu_utils import PieWidget

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
        pie_icon_radius_px: int = PIE_ICON_RADIUS_PX,
        color: QColor = QColor(55, 55, 55, 230),
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self._controller = controller
        self.widget = PieWidget(
            controller,
            values,
            pie_radius_px,
            pie_icon_radius_px,
            color
        )

    def on_key_press(self) -> None:
        self._controller.refresh()
        cursor = Krita.get_cursor()
        self.start = (cursor.x(), cursor.y())
        self.widget.move_center(*self.start)
        self.widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        cursor = Krita.get_cursor()
        angle = math.degrees(math.atan2(
            (-self.start[0] + cursor.x()),
            (self.start[1] - cursor.y())
        ))
        angle %= 360
        label = self.widget.labels.closest(round(angle))
        self._controller.set_value(label.value)
        self.widget.hide()
