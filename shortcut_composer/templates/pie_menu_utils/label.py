# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union, Type, Any
from dataclasses import dataclass

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import (
    QFont,
    QPixmap,
    QColor,
    QIcon,
    QFontDatabase,
    QPaintEvent,
)
from PyQt5.QtWidgets import QLabel, QWidget

from api_krita.pyqt import Painter, Text, PixmapTransform
from .animation_progress import AnimationProgress
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

    def __post_init__(self):
        self.activation_progress = AnimationProgress(speed_scale=1, steep=1)

    def create_label_widget(
        self,
        style: PieStyle,
        parent: QWidget
    ) -> 'LabelWidget':
        """Return LabelPainter which can display this label."""
        if self.display_value is None:
            raise ValueError(f"Label {self} is not valid")

        painter_type: Type[LabelWidget] = {
            QPixmap: ImageLabelWidget,
            Text: TextLabelWidget,
            QIcon: IconLabelWidget,
        }[type(self.display_value)]

        return painter_type(self, style, parent)


class LabelWidget(QWidget):
    """Displays a `label` inside of `widget` using given `style`."""

    def __init__(
        self,
        label: Label,
        style: PieStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)
        self._label = label
        self._parent = parent
        self._style = style
        self.setCursor(Qt.DragMoveCursor)

        size = self._style.icon_radius*2
        self.setGeometry(0, 0, size, size)

    @property
    def center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._style.icon_radius, self._style.icon_radius)

    def move_to_label(self) -> None:
        """Move the widget by providing a new center point."""
        self.move(self._label.center-self.center)  # type: ignore


class TextLabelWidget(LabelWidget):
    """Displays a `label` which holds text."""

    def __init__(self, label: Label, style: PieStyle, parent: QWidget) -> None:
        super().__init__(label, style, parent)
        self._pyqt_label = self._create_pyqt_label()

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint the entire widget using the Painter wrapper.

        Paint a background behind a label and its border.
        """
        with Painter(self, event) as painter:
            painter.paint_wheel(
                center=self.center,
                outer_radius=self._style.icon_radius,
                color=self._style.icon_color,
            )
            painter.paint_wheel(
                center=self.center,
                outer_radius=self._style.icon_radius,
                color=self._style.border_color,
                thickness=self._style.border_thickness,
            )

    def _create_pyqt_label(self) -> QLabel:
        """Create and show a new Qt5 label. Does not need redrawing."""
        to_display = self._label.display_value

        if not isinstance(to_display, Text):
            raise TypeError("Label supposed to be text.")

        heigth = round(self._style.icon_radius*0.8)

        label = QLabel(self)
        label.setText(to_display.value)
        label.setFont(self._font)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, round(heigth*2), round(heigth))
        label.move(self.center.x()-heigth,
                   self.center.y()-heigth//2)
        label.setStyleSheet(f'''
            background-color:rgba({self._color_to_str(self._style.icon_color)});
            color:rgba({self._color_to_str(to_display.color)});
        ''')

        label.show()
        return label

    @property
    def _font(self) -> QFont:
        """Return font which to use in pyqt label."""
        font = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font.setPointSize(self._style.font_size)
        font.setBold(True)
        return font

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}'''


class ImageLabelWidget(LabelWidget):
    """Displays a `label` which holds an image."""

    def __init__(self, label: Label, style: PieStyle, parent: QWidget) -> None:
        super().__init__(label, style, parent)
        self.ready_image = self._prepare_image()

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint the entire widget using the Painter wrapper.

        Paint a background behind a label its border, and image itself.
        """
        with Painter(self, event) as painter:
            painter.paint_wheel(
                center=self.center,
                outer_radius=self._style.icon_radius,
                color=self._style.icon_color
            )
            painter.paint_wheel(
                center=self.center,
                outer_radius=(
                    self._style.icon_radius-self._style.border_thickness//2),
                color=self._style.border_color,
                thickness=self._style.border_thickness,
            )
            painter.paint_pixmap(self.center, self.ready_image)

    def _prepare_image(self) -> QPixmap:
        """Return image after scaling and reshaping it to circle."""
        to_display = self._label.display_value

        if not isinstance(to_display, QPixmap):
            raise TypeError("Label supposed to be QPixmap.")

        rounded_image = PixmapTransform.make_pixmap_round(to_display)
        return PixmapTransform.scale_pixmap(
            pixmap=rounded_image,
            size_px=round(self._style.icon_radius*1.8)
        )


class IconLabelWidget(ImageLabelWidget):
    """Displays a `label` which holds an icon."""

    def _prepare_image(self) -> QPixmap:
        """Return icon after scaling it to fix QT_SCALE_FACTOR."""
        to_display = self._label.display_value

        if not isinstance(to_display, QIcon):
            raise TypeError("Label supposed to be QIcon.")

        size = round(self._style.icon_radius*1.1)
        return PixmapTransform.scale_pixmap(
            pixmap=to_display.pixmap(size, size),
            size_px=size
        )
