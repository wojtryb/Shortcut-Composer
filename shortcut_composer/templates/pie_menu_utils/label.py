# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union, Type, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon, QFontDatabase
from PyQt5.QtWidgets import QLabel, QWidget

from api_krita.pyqt import Painter, Text, PixmapTransform
from .pie_style import PieStyle


@dataclass
class Label:
    """
    Paintable representation of value in PieWidget.

    - `value` -- Value to set using the controller
    - `center -- Label position in widget coordinates
    - `angle` -- Angle in degrees in relation to widget center. Angles are
                 counted clockwise with 0 being the top of widget
    - `display_value` -- `value` representation to display. Can be
                         either a colored text or an image

    `display_value` can also be accessed using `text` and `image`
    properties, which return None when the value does not exist or is
    not of required type.

    Label can be displayed with LabelPainter, returned by get_painter().
    """

    value: Any
    center: QPoint = QPoint(0, 0)
    angle: int = 0
    display_value: Union[QPixmap, QIcon, Text, None] = None

    def get_painter(self, widget: QWidget, style: PieStyle) -> 'LabelPainter':
        """Return LabelPainter which can display this label."""
        if self.display_value is None:
            raise ValueError(f"Label {self} is not valid")

        painter_type: Type[LabelPainter] = {
            QPixmap: ImageLabelPainter,
            Text: TextLabelPainter,
            QIcon: IconPainter,
        }[type(self.display_value)]

        return painter_type(self, widget, style)


@dataclass
class LabelPainter(ABC):
    """Displays a `label` inside of `widget` using given `style`."""

    label: Label
    widget: QWidget
    style: PieStyle

    @abstractmethod
    def paint(self, painter: Painter) -> None: """Paint a label."""


@dataclass
class TextLabelPainter(LabelPainter):
    """Displays a `label` which holds text."""

    def __post_init__(self):
        self._pyqt_label = self._create_pyqt_label()

    def paint(self, painter: Painter):
        """Paint a background behind a label and its border."""
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
        """Create and show a new Qt5 label. Does not need redrawing."""
        to_display = self.label.display_value

        if not isinstance(to_display, Text):
            raise TypeError("Label supposed to be text.")

        heigth = round(self.style.icon_radius*0.8)

        label = QLabel(self.widget)
        label.setText(to_display.value)
        label.setFont(self._font)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, round(heigth*2), round(heigth))
        label.move(self.label.center.x()-heigth,
                   self.label.center.y()-heigth//2)
        label.setStyleSheet(f'''
            background-color:rgba({self._color_to_str(self.style.icon_color)});
            color:rgba({self._color_to_str(to_display.color)});
        ''')

        label.show()
        return label

    @property
    def _font(self) -> QFont:
        """Return font which to use in pyqt label."""
        font = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font.setPointSize(self.style.font_size)
        font.setBold(True)
        return font

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}'''


@dataclass
class ImageLabelPainter(LabelPainter):
    """Displays a `label` which holds an image."""

    def __post_init__(self):
        self.ready_image = self._prepare_image()

    def paint(self, painter: Painter):
        """Paint a background behind a label its border, and image itself."""
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

    def _prepare_image(self) -> QPixmap:
        """Return image after scaling and reshaping it to circle."""
        to_display = self.label.display_value

        if not isinstance(to_display, QPixmap):
            raise TypeError("Label supposed to be QPixmap.")

        rounded_image = PixmapTransform.make_pixmap_round(to_display)
        return PixmapTransform.scale_pixmap(
            pixmap=rounded_image,
            size_px=round(self.style.icon_radius*1.8)
        )


class IconPainter(ImageLabelPainter):
    """Displays a `label` which holds an icon."""

    def _prepare_image(self) -> QPixmap:
        """Return icon after scaling it to fix QT_SCALE_FACTOR."""
        to_display = self.label.display_value

        if not isinstance(to_display, QIcon):
            raise TypeError("Label supposed to be QIcon.")

        size = round(self.style.icon_radius*1.1)
        return PixmapTransform.scale_pixmap(
            pixmap=to_display.pixmap(size, size),
            size_px=size
        )
