from typing import List, TypeVar, Generic, Union

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QFont,
    QPixmap,
    QImage,
    QBrush,
    QWindow
)

from shortcut_composer_config import SHORT_VS_LONG_PRESS_TIME
from core_components import Controller, Instruction
from input_adapter import PluginAction

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
        label.setGeometry(pos.x(), pos.y(), 100, 100)
        label.setStyleSheet(
            "background-color:rgba(47, 47, 47, 255);"
            "color: white;"
            "border-radius: 50px;"
            "border: 3px rgba(60, 60, 60, 255);"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)

        if isinstance(value, str):
            label.setText(value)
        elif isinstance(value, QPixmap):
            rounded_image = self._make_pixmap_round(value, size=100)
            label.setPixmap(rounded_image)
        label.show()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.eraseRect(event.rect())
        self.painter.setRenderHints(QPainter.HighQualityAntialiasing)
        self._paint_wheel()
        label = self._controller.get_label(self._values[0])
        self._paint_label(QPoint(100, 100), label)
        self.painter.end()

    @staticmethod
    def _make_pixmap_round(pixmap: QPixmap, size=100) -> QPixmap:
        image = pixmap.toImage()
        image.convertToFormat(QImage.Format_ARGB32)

        imgsize = min(image.width(), image.height())
        out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)

        brush = QBrush(image)
        painter = QPainter(out_img)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawEllipse(0, 0, imgsize, imgsize)
        painter.end()

        pixel_ratio = QWindow().devicePixelRatio()
        pixmap = QPixmap.fromImage(out_img)
        pixmap.setDevicePixelRatio(pixel_ratio)
        new_size = round(size * pixel_ratio)
        pixmap = pixmap.scaled(
            new_size,
            new_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        return pixmap


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
