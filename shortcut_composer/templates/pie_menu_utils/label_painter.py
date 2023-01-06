from abc import ABC, abstractmethod
from dataclasses import dataclass

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from api_krita.pyqt import Painter, make_pixmap_round, scale_pixmap
from .label import Label
from .pie_style import PieStyle


@dataclass
class LabelPainter(ABC):
    widget: QWidget
    style: PieStyle
    label: Label

    @abstractmethod
    def paint(self, painter: Painter) -> None: ...


def pick_correct_painter(
    widget: QWidget,
    style: PieStyle,
    label: Label,
) -> LabelPainter:
    if isinstance(label.display_value, str):
        return TextLabelPainter(widget, style, label)
    elif isinstance(label.display_value, QPixmap):
        return ImageLabelPainter(widget, style, label)
    raise TypeError("Wrong type")


@dataclass
class TextLabelPainter(LabelPainter):

    def __post_init__(self):
        self._pyqt_label = self._create_pyqt_label()

    def paint(self, painter: Painter):
        painter.paint_wheel(
            center=self.label.center,
            outer_radius=self.style.icon_radius,
            color=self.style.color
        )
        painter.paint_wheel(
            center=self.label.center,
            outer_radius=self.style.icon_radius-self.style.border_thickness//2,
            color=self.style.border_color,
            thickness=self.style.border_thickness,
        )

    def _create_pyqt_label(self):
        if not isinstance(self.label.display_value, str):
            raise TypeError("Label supposed to be text.")

        label = QLabel("text label", self.widget)
        label.setFont(QFont('Times', 20))
        label.adjustSize()
        small_radius = round(self.style.icon_radius*0.6)
        label.setGeometry(
            round(self.label.center.x()-small_radius),
            round(self.label.center.y()-small_radius),
            round(small_radius*2),
            round(small_radius*2)
        )
        label.setStyleSheet(
            f"""background-color:rgba(
                {self.style.color.red()},
                {self.style.color.green()},
                {self.style.color.blue()},
                {self.style.color.alpha()}
            );"""
            "color: white;"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setText(self.label.display_value)

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
            color=self.style.border_color
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
