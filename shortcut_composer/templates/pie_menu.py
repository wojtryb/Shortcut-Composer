from typing import List, TypeVar, Generic
import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (
    QColor,
)

from shortcut_composer_config import (
    SHORT_VS_LONG_PRESS_TIME,
    PIE_ICON_RADIUS_PX,
    PIE_RADIUS_PX,
)
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita import Krita
from api_krita.pyqt import Painter, Label, pick_correct_label

T = TypeVar('T')


class MyWidget(QWidget):
    def __init__(
        self,
        controller: Controller,
        values: list,
        pie_radius_px: int,
        pie_icon_radius_px: int,
        color: QColor,
        parent=None
    ):
        QWidget.__init__(self, parent)
        self._controller = controller
        self._values = values
        self._pie_radius_px = pie_radius_px
        self._pie_icon_radius_px = pie_icon_radius_px
        self._color = color

        self.setWindowFlags(
            self.windowFlags() |
            Qt.Window |  # type: ignore
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Pie Menu")
        size = PIE_RADIUS_PX*2
        self.setGeometry(0, 0, size, size)

        self.labels = self._create_labels()
        self.changed = False

    @property
    def center(self) -> QPoint:
        return QPoint(self._pie_radius_px, self._pie_radius_px)

    def move_center(self, x: int, y: int) -> None:
        self.move(x-self._pie_radius_px, y-self._pie_radius_px)

    def show(self) -> None:
        super().show()
        self.changed = True

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if not self.changed:
            return

        self.painter = Painter(self, event)
        self.painter.paint_wheel(
            center=self.center,
            outer_radius=self._pie_radius_px-self._pie_icon_radius_px*0.7,
            color=self._color,
            fill_part=0.3,
        )
        for label in self.labels:
            label.paint(self.painter)

        self.painter.end()
        self.changed = False

    def _center_from_angle(self, angle: int, distance: int) -> QPoint:
        rad_angle = math.radians(angle)
        return QPoint(
            round(self._pie_radius_px + distance*math.sin(rad_angle)),
            round(self._pie_radius_px - distance*math.cos(rad_angle)),
        )

    def _create_labels(self) -> List[Label]:
        labels = []

        iterator = range(0, 360, round(360/len(self._values)))
        for value, angle in zip(self._values, iterator):
            distance = self._pie_radius_px-self._pie_icon_radius_px
            label_center = self._center_from_angle(angle, distance)

            labels.append(pick_correct_label(
                widget=self,
                center=label_center,
                radius=self._pie_icon_radius_px,
                value=self._controller.get_label(value),
                bg_color=QColor(47, 47, 47, 255)
            ))
        return labels


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
        self.widget = MyWidget(
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
