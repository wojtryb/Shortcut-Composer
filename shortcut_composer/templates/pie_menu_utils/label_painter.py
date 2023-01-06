from abc import ABC, abstractmethod
from dataclasses import dataclass

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from shortcut_composer_config import ICON_RADIUS_PX
from api_krita.pyqt import Painter, make_pixmap_round, scale_pixmap, Text
from .label import Label


def create_painter(label: Label, widget: QWidget) -> "LabelPainter":
    if isinstance(label.display_value, Text):
        return TextLabelPainter(widget, label)
    elif isinstance(label.display_value, QPixmap):
        return ImageLabelPainter(widget, label)
    raise TypeError(f"Unknown label type {type(label.display_value)}")


@dataclass
class LabelPainter(ABC):
    widget: QWidget
    label: Label

    @property
    def style(self):
        return self.label.style

    @abstractmethod
    def paint(self, painter: Painter) -> None: ...


@dataclass
class TextLabelPainter(LabelPainter):

    def __post_init__(self):
        self._pyqt_label = self._create_pyqt_label()

    def paint(self, painter: Painter):
        painter.paint_wheel(
            center=self.label.center,
            outer_radius=self.style.icon_radius,
            color=self.style.icon_color
        )
        painter.paint_wheel(
            center=self.label.center,
            outer_radius=self.style.icon_radius,
            color=self.style.border_color,
            thickness=self.style.border_thickness,
        )

    def _create_pyqt_label(self):
        if not isinstance(self.label.display_value, Text):
            raise TypeError("Label supposed to be text.")

        label = QLabel("text label", self.widget)
        label.setFont(QFont(
            'Helvetica',
            round(ICON_RADIUS_PX*0.45),
            QFont.Bold))
        label.adjustSize()
        small_radius = round(self.style.icon_radius*0.4)
        label.setGeometry(
            round(self.label.center.x()-small_radius*2),
            round(self.label.center.y()-small_radius),
            round(small_radius*4),
            round(small_radius*2)
        )
        label.setStyleSheet(
            f"""background-color:rgba(
                {self.style.icon_color.red()},
                {self.style.icon_color.green()},
                {self.style.icon_color.blue()},
                {self.style.icon_color.alpha()}
            );
            color:rgba(
                {self.label.display_value.color.red()},
                {self.label.display_value.color.green()},
                {self.label.display_value.color.blue()},
                {self.label.display_value.color.alpha()}
            );"""
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setText(self.label.display_value.text)

        label.show()
        return label


@dataclass
class ImageLabelPainter(LabelPainter):
    def __post_init__(self):
        self.ready_image = self._prepare_image()

    def paint(self, painter: Painter):
        painter.paint_wheel(
            center=self.label.center,
            outer_radius=self.style.icon_radius,
            color=self.style.icon_color
        )
        painter.paint_wheel(
            center=self.label.center,
            outer_radius=self.style.icon_radius-self.style.border_thickness//2,
            color=self.style.border_color,
            thickness=self.style.border_thickness,
        )
        painter.paint_pixmap(self.label.center, self.ready_image)

    def _prepare_image(self):
        if not isinstance(self.label.display_value, QPixmap):
            raise TypeError("Label supposed to be pixmap.")

        rounded_image = make_pixmap_round(self.label.display_value)
        return scale_pixmap(
            pixmap=rounded_image,
            size_px=round(self.style.icon_radius*1.8)
        )
