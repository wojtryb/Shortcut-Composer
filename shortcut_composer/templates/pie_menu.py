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

from shortcut_composer_config import SHORT_VS_LONG_PRESS_TIME, PIE_ICON_SIZE_PX
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita import pyqt

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

    def _paint_wheel(self):
        path = QPainterPath()
        path.addEllipse(QPoint(100, 100), 100, 100)
        path.addEllipse(QPoint(100, 100), 80, 80)
        self.painter.fillPath(path, QColor(100, 100, 100, 50))

    def _paint_label(self, pos: QPoint, value: Union[str, QPixmap]):
        label = QLabel("text label", self)
        label.setFont(QFont('Times', 20))
        label.adjustSize()
        label.setGeometry(pos.x(), pos.y(), PIE_ICON_SIZE_PX, PIE_ICON_SIZE_PX)
        label.setStyleSheet(
            "background-color:rgba(47, 47, 47, 255);"
            "color: white;"
            f"border-radius: {PIE_ICON_SIZE_PX//2}px;"
            "border: 3px rgba(60, 60, 60, 255);"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)

        if isinstance(value, str):
            label.setText(value)
        elif isinstance(value, QPixmap):
            rounded_image = pyqt.make_pixmap_round(value)
            label.setPixmap(pyqt.scale_pixmap(
                rounded_image,
                size_px=PIE_ICON_SIZE_PX
            ))
        label.show()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.eraseRect(event.rect())
        self.painter.setRenderHints(QPainter.Antialiasing)
        self._paint_wheel()
        label = self._controller.get_label(self._values[0])
        self._paint_label(QPoint(100, 100), label)
        self.painter.end()


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
        self.widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        self.widget.hide()
