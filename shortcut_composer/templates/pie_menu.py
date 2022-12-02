from typing import List, TypeVar, Generic, Union
import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
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
    def __init__(self, controller: Controller, values: list, parent=None):
        QWidget.__init__(self, parent)
        self._controller = controller
        self._values = values

        self.setWindowFlags(
            self.windowFlags() |
            Qt.Window |  # type: ignore
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Pie Menu")
        self.setGeometry(0, 0, self.center_value*2, self.center_value*2)

        self.changed = False

    @property
    def center_value(self):
        return PIE_ICON_RADIUS_PX + PIE_RADIUS_PX

    @property
    def center(self):
        return QPoint(self.center_value, self.center_value)

    def move_center(self, x: int, y: int):
        self.move(x-self.center_value, y-self.center_value)

    def _paint_main_wheel(self):
        path = QPainterPath()
        path.addEllipse(
            self.center,
            PIE_RADIUS_PX,
            PIE_RADIUS_PX)
        path.addEllipse(
            self.center,
            PIE_RADIUS_PX*0.7,
            PIE_RADIUS_PX*0.7)
        self.painter.fillPath(path, QColor(100, 100, 100, 50))

    def _paint_label(self, center: QPoint, value: Union[str, QPixmap]):
        path = QPainterPath()
        path.addEllipse(
            center,
            PIE_ICON_RADIUS_PX,
            PIE_ICON_RADIUS_PX)
        self.painter.fillPath(path, QColor(47, 47, 47, 255))

        if isinstance(value, QPixmap):
            rounded_image = pyqt.make_pixmap_round(value)
            scaled_image = pyqt.scale_pixmap(
                rounded_image,
                size_px=PIE_ICON_RADIUS_PX*2
            )
            self.painter.drawPixmap(
                QPoint(
                    center.x() - PIE_ICON_RADIUS_PX,
                    center.y() - PIE_ICON_RADIUS_PX
                ),
                scaled_image
            )
        elif isinstance(value, str):
            label = QLabel("text label", self)
            label.setFont(QFont('Times', 20))
            label.adjustSize()
            label.setGeometry(
                round(center.x()-PIE_ICON_RADIUS_PX*0.6),
                round(center.y()-PIE_ICON_RADIUS_PX*0.6),
                round(PIE_ICON_RADIUS_PX*1.2),
                round(PIE_ICON_RADIUS_PX*1.2))
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
            self.painter = QPainter(self)
            self.painter.eraseRect(event.rect())
            self.painter.setRenderHints(QPainter.Antialiasing)
            self._paint_main_wheel()
            iterator = range(0, 360, round(360/len(self._values)))
            for value, angle in zip(self._values, iterator):
                label = self._controller.get_label(value)
                point = self._center_from_angle(angle)
                self._paint_label(point, label)
            self.painter.end()
            self.changed = False

    def _center_from_angle(self, angle: int):
        rad_angle = math.radians(angle)
        return QPoint(
            round(self.center_value + PIE_RADIUS_PX*math.sin(rad_angle)),
            round(self.center_value - PIE_RADIUS_PX*math.cos(rad_angle)),
        )


class PieMenu(PluginAction, Generic[T]):

    def __init__(
        self, *,
        name: str,
        controller: Controller,
        values: List[T],
        instructions: List[Instruction] = [],
        short_vs_long_press_time: float = SHORT_VS_LONG_PRESS_TIME
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self.widget = MyWidget(controller, values)

    def on_key_press(self) -> None:
        cursor = Krita.get_cursor()
        self.widget.move_center(cursor.x(), cursor.y())
        self.widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        self.widget.hide()
