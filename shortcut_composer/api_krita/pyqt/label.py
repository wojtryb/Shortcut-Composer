from typing import Union, Protocol, Any

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import QPoint, Qt

from .painter import Painter
from .pixmap_transform import make_pixmap_round, scale_pixmap


class Label(Protocol):
    center: QPoint
    radius: int
    value: Any
    bg_color: QColor
    def paint(self, painter: Painter): ...


def pick_correct_label(
    widget: QWidget,
    center: QPoint,
    radius: int,
    value: Any,
    display_value: Union[str, QPixmap],
    bg_color: QColor = QColor(47, 47, 47, 255),
) -> Label:
    if isinstance(display_value, str):
        return TextLabel(widget, center, radius, value, display_value, bg_color)
    elif isinstance(display_value, QPixmap):
        return ImageLabel(widget, center, radius, value, display_value, bg_color)


class TextLabel:
    def __init__(
        self,
        widget: QWidget,
        center: QPoint,
        radius: int,
        value: Any,
        text: str,
        bg_color: QColor = QColor(47, 47, 47, 255)
    ):
        self.widget = widget
        self.center = center
        self.radius = radius
        self.value = value
        self.text = text
        self.bg_color = bg_color
        self._pyqt_label = self._create_pyqt_label()

    def paint(self, painter: Painter):
        painter.paint_wheel(
            center=self.center,
            outer_radius=self.radius,
            color=self.bg_color
        )

    def _create_pyqt_label(self, ):
        label = QLabel("text label", self.widget)
        label.setFont(QFont('Times', 20))
        label.adjustSize()
        small_radius = round(self.radius*0.6)
        label.setGeometry(
            round(self.center.x()-small_radius),
            round(self.center.y()-small_radius),
            round(small_radius*2),
            round(small_radius*2)
        )
        label.setStyleSheet(
            f"""background-color:rgba(
                {self.bg_color.red()},
                {self.bg_color.green()},
                {self.bg_color.blue()},
                {self.bg_color.alpha()}
            );"""
            "color: white;"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setText(self.text)

        label.show()
        return label


class ImageLabel:
    def __init__(
        self,
        widget: QWidget,
        center: QPoint,
        radius: int,
        value: Any,
        picture: QPixmap,
        bg_color: QColor = QColor(47, 47, 47, 255)
    ):
        self.widget = widget
        self.center = center
        self.radius = radius
        self.value = value
        self.picture = picture
        self.bg_color = bg_color

    def paint(self, painter: Painter):
        painter.paint_wheel(
            center=self.center,
            outer_radius=self.radius,
            color=self.bg_color
        )

        rounded_image = make_pixmap_round(self.picture)
        scaled_image = scale_pixmap(
            pixmap=rounded_image,
            size_px=round(self.radius*1.8)
        )
        painter.paint_pixmap(self.center, scaled_image)
