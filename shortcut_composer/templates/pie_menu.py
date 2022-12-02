from typing import List, TypeVar, Generic, Union
import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import (
    QColor,
    QFont,
    QPixmap,
)

from shortcut_composer_config import (
    SHORT_VS_LONG_PRESS_TIME,
    PIE_ICON_RADIUS_PX,
    PIE_RADIUS_PX,
)
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita import Krita, pyqt

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

        self.changed = False

    @property
    def center(self):
        return QPoint(self._pie_radius_px, self._pie_radius_px)

    def move_center(self, x: int, y: int):
        self.move(x-self._pie_radius_px, y-self._pie_radius_px)

    def _paint_label(self, center: QPoint, value: Union[str, QPixmap]):
        self.painter.paint_wheel(
            center=center,
            outer_radius=self._pie_icon_radius_px,
            color=QColor(47, 47, 47, 255)
        )
        if isinstance(value, QPixmap):
            rounded_image = pyqt.make_pixmap_round(value)
            scaled_image = pyqt.scale_pixmap(
                rounded_image,
                size_px=self._pie_icon_radius_px*2
            )
            self.painter.paint_pixmap(center, scaled_image)
        elif isinstance(value, str):
            label = QLabel("text label", self)
            label.setFont(QFont('Times', 20))
            label.adjustSize()
            label.setGeometry(
                round(center.x()-self._pie_icon_radius_px*0.6),
                round(center.y()-self._pie_icon_radius_px*0.6),
                round(self._pie_icon_radius_px*1.2),
                round(self._pie_icon_radius_px*1.2))
            label.setStyleSheet(
                "background-color:rgba(47, 47, 47, 255);"
                "color: white;"
            )
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            label.setText(value)

            label.show()

    def show(self) -> None:
        super().show()
        self.changed = True

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.changed:
            self.painter = pyqt.Painter(self, event)
            self.painter.paint_wheel(
                center=self.center,
                outer_radius=self._pie_radius_px-self._pie_icon_radius_px*0.7,
                color=self._color,
                fill_part=0.3,
            )
            iterator = range(0, 360, round(360/len(self._values)))
            for value, angle in zip(self._values, iterator):
                label = self._controller.get_label(value)
                distance = self._pie_radius_px-self._pie_icon_radius_px
                point = self._center_from_angle(angle, distance)
                self._paint_label(point, label)
            self.painter.end()
            self.changed = False

    def _center_from_angle(self, angle: int, distance: int):
        rad_angle = math.radians(angle)
        return QPoint(
            round(self._pie_radius_px + distance*math.sin(rad_angle)),
            round(self._pie_radius_px - distance*math.cos(rad_angle)),
        )


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
