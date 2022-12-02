from typing import List, TypeVar, Generic

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
        color: QColor = QColor(100, 100, 100, 150),
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self.widget = PieWidget(
            controller,
            values,
            pie_radius_px,
            pie_icon_radius_px,
            color
        )

    def on_key_press(self) -> None:
        cursor = Krita.get_cursor()
        self.widget.move_center(cursor.x(), cursor.y())
        self.widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        self.widget.hide()
