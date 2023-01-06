from typing import List, TypeVar, Generic, Union

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
        self.setGeometry(0, 0, PIE_RADIUS_PX*2, PIE_RADIUS_PX*2)

        self.changed = False

    def _paint_wheel(self):
        path = QPainterPath()
        path.addEllipse(
            QPoint(PIE_RADIUS_PX, PIE_RADIUS_PX),
            PIE_RADIUS_PX,
            PIE_RADIUS_PX)
        path.addEllipse(
            QPoint(PIE_RADIUS_PX, PIE_RADIUS_PX),
            PIE_RADIUS_PX*0.7,
            PIE_RADIUS_PX*0.7)
        self.painter.fillPath(path, QColor(100, 100, 100, 50))

    def _paint_label(self, pos: QPoint, value: Union[str, QPixmap]):
        path = QPainterPath()
        path.addEllipse(
            pos,
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
                    pos.x() - PIE_ICON_RADIUS_PX,
                    pos.y() - PIE_ICON_RADIUS_PX
                ),
                scaled_image
            )
        elif isinstance(value, str):
            label = QLabel("text label", self)
            label.setFont(QFont('Times', 20))
            label.adjustSize()
            label.setGeometry(
                round(pos.x()-PIE_ICON_RADIUS_PX*0.6),
                round(pos.y()-PIE_ICON_RADIUS_PX*0.6),
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
            self._paint_wheel()
            label = self._controller.get_label(self._values[0])
            self._paint_label(QPoint(100, 100), label)
            self.painter.end()
            self.changed = False


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
        self.widget.move(cursor.x()-PIE_RADIUS_PX, cursor.y()-PIE_RADIUS_PX)
        self.widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        self.widget.hide()
