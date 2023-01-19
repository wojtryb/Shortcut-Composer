# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional
from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPaintEvent, QDragMoveEvent, QDragEnterEvent
from PyQt5.QtWidgets import QPushButton

from api_krita import Krita
from api_krita.pyqt import Painter, AnimatedWidget
from composer_utils import Config
from .pie_style import PieStyle
from .widget_holder import WidgetHolder
from .label import Label
from .pie_painter import PiePainter
from .label_widgets import LabelWidget, create_label_widget
from .circle_points import CirclePoints


class EditMode:
    def __get__(self, obj, _):
        return obj._edit_mode

    def __set__(self, obj: 'PieWidget', mode_to_set: bool):
        if not mode_to_set and obj._edit_mode:
            self._write_settings(obj)

        obj._edit_mode = mode_to_set
        if mode_to_set:
            obj.accept_button.show()
        else:
            obj.accept_button.hide()

    def _write_settings(self, obj: 'PieWidget'):
        if not obj.labels or obj._related_config is None:
            return

        values = [widget.label.value for widget in obj.widget_holder]
        if isinstance(values[0], Enum):
            obj._related_config.write(Config.format_enums(values))
        else:
            obj._related_config.write('\t'.join(values))


class PieWidget(AnimatedWidget):
    """
    PyQt5 widget with icons on ring that can be selected by hovering.

    Methods inherits from QWidget used by other components:
    - show() - displays the widget
    - hide() - hides the widget
    - repaint() - updates widget display after its data was changed

    Overrides paintEvent(QPaintEvent) which tells how the widget looks

    - Paints the widget: its base, and active pie and deadzone indicator
    - Wraps Labels with LabelWidgets which activated, paint them
    - Extends widget interface to allow moving the widget on screen by
      providing the widget center.
    """

    edit_mode = EditMode()

    def __init__(
        self,
        style: PieStyle,
        labels: List[Label],
        related_config: Optional[Config],
        parent=None
    ):
        super().__init__(parent, Config.PIE_ANIMATION_TIME.read())

        self._style = style
        self.labels = labels
        self._related_config = related_config
        self.children_widgets = self._create_children_holder()
        self.widget_holder = self._put_children_in_holder()
        self._edit_mode = False
        self._circle_points: CirclePoints

        size = self._style.widget_radius*2
        self.setGeometry(0, 0, size, size)

        self.accept_button = QPushButton(Krita.get_icon("dialog-ok"), "", self)
        self.accept_button.hide()
        radius = round(self.deadzone*0.9)
        self.accept_button.setGeometry(
            self._center.x() - radius,
            self._center.y() - radius,
            radius*2,
            radius*2)
        self.accept_button.setStyleSheet(f"""
            border-radius: {radius};
            background-color : green;
            qproperty-iconSize: {round(radius*1.5)}px;
        """)
        self.accept_button.clicked.connect(self.hide)

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Popup |
            Qt.FramelessWindowHint |
            Qt.NoDropShadowWindowHint))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CrossCursor)

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self.size().width()//2, self.size().height()//2)

    @property
    def center_global(self) -> QPoint:
        """Return point with center widget's point in screen coordinates."""
        return self.pos() + self._center  # type: ignore

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._style.deadzone_radius

    def hide(self):
        self.edit_mode = False
        super().hide()

    def move_center(self, new_center: QPoint) -> None:
        """Move the widget by providing a new center point."""
        self.move(new_center-self._center)  # type: ignore

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            PiePainter(painter, self.labels, self._style)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        self.edit_mode = True
        self._circle_points = CirclePoints(
            center=self._center,
            radius=self._style.pie_radius)
        e.accept()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        pos = e.pos()
        source_widget = e.source()

        if (self._circle_points.distance(pos) < self._style.deadzone_radius
                or not isinstance(source_widget, LabelWidget)):
            return e.accept()

        angle = self._circle_points.angle_from_point(pos)
        widget = self.widget_holder.on_angle(angle)
        if widget == source_widget:
            return e.accept()

        self.widget_holder.swap(widget, source_widget)
        self.repaint()
        e.accept()

    def _create_children_holder(self) -> List[LabelWidget]:
        """Create LabelWidgets that represent the labels."""
        children: List[LabelWidget] = []
        for label in self.labels:
            children.append(create_label_widget(label, self._style, self))
        return children

    def _put_children_in_holder(self) -> WidgetHolder:
        children = self.children_widgets
        center = QPoint(self._style.widget_radius, self._style.widget_radius)
        circle_points = CirclePoints(
            center=center,
            radius=self._style.pie_radius)

        angle_iterator = circle_points.iterate_over_circle(len(children))
        label_holder = WidgetHolder()
        for child, (angle, point) in zip(children, angle_iterator):
            child.label.angle = angle
            child.label.center = point
            child.move_to_label()
            label_holder.add(child)

        return label_holder
