from abc import ABC, abstractmethod
from dataclasses import dataclass

from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt

from api_krita import pyqt
from api_krita.pyqt import Painter, Text
from .label import Label
from .pie_style import PieStyle


def create_painter(label: Label, style: PieStyle, widget: QWidget) \
        -> 'LabelPainter':
    if isinstance(label.display_value, Text):
        return TextLabelPainter(widget, style, label)
    elif isinstance(label.display_value, QPixmap):
        return ImageLabelPainter(widget, style, label)
    raise TypeError(f"Unknown label type: {type(label.display_value)}")


@dataclass
class LabelPainter(ABC):

    widget: QWidget
    style: PieStyle
    label: Label

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
            color=self.style.icon_color,
        )
        painter.paint_wheel(
            center=self.label.center,
            outer_radius=self.style.icon_radius,
            color=self.style.border_color,
            thickness=self.style.border_thickness,
        )

    def _create_pyqt_label(self) -> QLabel:
        if not isinstance(self.label.display_value, Text):
            raise TypeError("Label supposed to be text.")

        font_size = round(self.style.icon_radius*0.45)
        heigth = round(self.style.icon_radius*0.8)

        label = QLabel(self.widget)
        label.setText(self.label.display_value.text)
        label.setFont(QFont('Helvetica', font_size, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, round(heigth*2), round(heigth))
        label.move(self.label.center.x()-heigth,
                   self.label.center.y()-heigth//2)
        label.setStyleSheet(f'''
            background-color:rgba({self._color_to_str(self.style.icon_color)});
            color:rgba({self._color_to_str(self.label.display_value.color)});
        ''')

        label.show()
        return label

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}'''


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

        rounded_image = pyqt.make_pixmap_round(self.label.display_value)
        return pyqt.scale_pixmap(
            pixmap=rounded_image,
            size_px=round(self.style.icon_radius*1.8)
        )
