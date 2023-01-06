from typing import List, TypeVar, Generic, Tuple, Union, Optional

from PyQt5.QtGui import QColor, QPixmap

from shortcut_composer_config import (
    SHORT_VS_LONG_PRESS_TIME,
    ICON_RADIUS_SCALE,
    PIE_RADIUS_SCALE,
    PIE_ACTIVE_COLOR,
    PIE_AREA_COLOR,
)
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita import Krita
from api_krita.pyqt import Text
from .pie_menu_utils import (
    AngleIterator,
    LabelHolder,
    PieManager,
    PieWidget,
    PieStyle,
    Label,
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
        pie_radius_scale: float = PIE_RADIUS_SCALE,
        icon_radius_scale: float = ICON_RADIUS_SCALE,
        area_color: QColor = PIE_AREA_COLOR,
        active_color: QColor = PIE_ACTIVE_COLOR,
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self._controller = controller

        self._style = PieStyle(
            pie_radius_scale=pie_radius_scale,
            icon_radius_scale=icon_radius_scale,
            area_color=area_color,
            active_color=active_color,
        )
        self._labels = self._create_labels(values)
        self._style.update_with_item_amount(len(self._labels))

        self._widget = PieWidget(self._labels, self._style)
        self._pie_manager = PieManager(self._widget, self._labels)

    def on_key_press(self) -> None:
        self._controller.refresh()
        cursor = Krita.get_cursor()
        self._widget.move_center(cursor.x(), cursor.y())
        self._pie_manager.start()
        self._widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        self._pie_manager.stop()
        self._widget.hide()
        if label := self._labels.active:
            self._controller.set_value(label.value)

    def _create_labels(self, values: List[T]) -> LabelHolder:
        icons = [self._try_get_icon(value) for value in values]

        label_list: List[Label] = []
        for value, icon in zip(values, icons):
            if icon:
                label_list.append(Label(value=value, display_value=icon))

        angle_iterator = AngleIterator(
            center_distance=self._style.widget_radius,
            radius=self._style.pie_radius,
            amount=len(label_list))

        for label, (angle, point) in zip(label_list, angle_iterator):
            label.angle = angle
            label.center = point

        label_holder = LabelHolder()
        for label in label_list:
            label_holder.add(label)
        return label_holder

    def _try_get_icon(self, value: T) -> Union[Text, QPixmap, None]:
        try:
            return self._controller.get_label(value)
        except KeyError:
            return None
