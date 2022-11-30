from typing import List, TypeVar, Generic

from shortcut_composer_config import SHORT_VS_LONG_PRESS_TIME
from core_components import Instruction
from input_adapter import PluginAction
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

from api_krita import Krita

T = TypeVar('T')


def mask_image(image: QImage, size=100):
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
    new_size = size * pixel_ratio
    pixmap = pixmap.scaled(
        new_size,
        new_size,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )

    return pixmap


class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowFlags(
            self.windowFlags() |
            Qt.Window |
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Pie Menu")
        self.radius = 300
        self.width = int(self.radius * 2)
        self.height = int(self.radius * 2)

    def _paint_wheel(self):
        path = QPainterPath()
        path.addEllipse(QPoint(100, 100), 100, 100)
        path.addEllipse(QPoint(100, 100), 80, 80)
        self.painter.fillPath(path, QColor(100, 100, 100, 50))

    def _paint_text_label(self):
        label = QLabel("text label", self)
        label.setFont(QFont('Times', 20))
        label.adjustSize()
        label.setGeometry(300, 100, 100, 100)
        label.setStyleSheet(
            "background-color:rgba(47, 47, 47, 255);"
            "color: white;"
            "border-radius: 50px;"
            "border: 3px rgba(60, 60, 60, 255);"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)

        label.setText("W pyte!")
        label.show()

    def _paint_preset_label(self):
        label = QLabel("paint label", self)
        label.adjustSize()
        label.setGeometry(500, 100, 100, 100)
        label.setStyleSheet(
            "background-color:rgba(0, 0, 0, 0);"
            "color: white;"
        )
        label.setAlignment(Qt.AlignCenter)
        presets = Krita.get_presets()
        image = list(presets.values())[5].image()
        pixels = mask_image(image, size=100)
        label.setPixmap(pixels)

        label.show()

    def _paint_icon_label(self):
        label = QLabel("icon label", self)
        label.adjustSize()
        label.setGeometry(500, 300, 100, 100)
        label.setStyleSheet(
            "background-color:rgba(47, 47, 47, 255);"
            "color: white;"
            "border-radius: 50px;"
            "border: 3px rgba(60, 60, 60, 255);"
        )
        label.setAlignment(Qt.AlignCenter)
        icon = Krita.get_icon("tool_crop")
        pixels = icon.pixmap(60, 60)
        label.setPixmap(pixels)

        label.show()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.eraseRect(event.rect())
        self.painter.setRenderHints(QPainter.HighQualityAntialiasing)
        self._paint_wheel()
        self._paint_text_label()
        self._paint_preset_label()
        self._paint_icon_label()
        self.painter.end()


class PieMenu(PluginAction, Generic[T]):

    def __init__(
        self, *,
        name: str,
        instructions: List[Instruction] = [],
        short_vs_long_press_time: float = SHORT_VS_LONG_PRESS_TIME
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)

    def on_key_press(self) -> None:
        self.widget = MyWidget()
        self.widget.show()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        super().on_every_key_release()
        self.widget.hide()
