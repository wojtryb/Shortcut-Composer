# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Optional, Generic, List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QPaintEvent)

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils import Config
from .pie_style import PieStyle
from .label import Label
from .label_widget import LabelWidget
from .pie_config import PieConfig
from .widget_utils import (
    WidgetHolder,
    CirclePoints,
    LabelHolder,
    PiePainter)

T = TypeVar('T')


class PieWidget(AnimatedWidget, BaseWidget, Generic[T]):
    """
    PyQt5 widget with icons on ring that can be selected by hovering.

    Methods inherits from QWidget used by other components:
    - show() - displays the widget
    - hide() - hides the widget
    - repaint() - updates widget display after its data was changed

    It uses LabelHolder to store children widgets representing the
    values user can pick. When the pie enters the edit mode, its
    children become draggable.

    By dragging children, user can change their order or remove them
    by moving them out of the widget. New children can be added by
    dragging them from other widgets.
    """

    def __init__(
        self,
        style: PieStyle,
        labels: List[Label[T]],
        config: PieConfig,
        parent=None
    ):
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        self.setGeometry(0, 0, style.widget_radius*2, style.widget_radius*2)

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.NoDropShadowWindowHint))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CrossCursor)

        self._style = style
        self._labels = labels
        self.config = config
        self.config.register_callback(self._reset)

        self.active: Optional[Label] = None
        self.is_edit_mode = False
        self._last_widget = None

        self.label_holder = LabelHolder(
            labels=self._labels,
            style=self._style,
            config=self.config,
            owner=self)
        self._circle_points: CirclePoints

        self.set_draggable(False)
        self._reset()

    def _reset(self):
        """Set widget geometry according to style and refresh CirclePoints."""
        widget_diameter = self._style.widget_radius*2
        self.setGeometry(0, 0, widget_diameter, widget_diameter)
        self._circle_points = CirclePoints(
            center=self.center,
            radius=self._style.pie_radius)

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._style.deadzone_radius

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            PiePainter(painter, self._labels, self._style, self.is_edit_mode)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Allow dragging the widgets while in edit mode."""
        if self.is_edit_mode:
            return e.accept()
        e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """Handle all children actions - order change, add and remove."""
        e.accept()
        source_widget = e.source()
        pos = e.pos()
        distance = self._circle_points.distance(pos)

        if not isinstance(source_widget, LabelWidget):
            # Drag incoming from outside the PieWidget ecosystem
            return

        if self.type and not isinstance(source_widget.label.value, self.type):
            # Label type does not match the type of pie menu
            return

        self._last_widget = source_widget
        if distance > self._style.widget_radius:
            # Dragged out of the PieWidget
            return self.label_holder.remove(source_widget.label)

        if not self._labels:
            # First label dragged to empty pie
            return self.label_holder.insert(0, source_widget.label)

        if distance < self._style.deadzone_radius:
            # Do nothing in deadzone
            return

        angle = self._circle_points.angle_from_point(pos)
        _a = self._widget_holder.on_angle(angle)

        if source_widget.label not in self.label_holder or not self._labels:
            # Dragged with unknown label
            index = self.label_holder.index(_a.label)
            return self.label_holder.insert(index, source_widget.label)

        _b = self._widget_holder.on_label(source_widget.label)
        if _a != _b:
            # Dragged existing label to a new location
            self.label_holder.swap(_a.label, _b.label)
            self.repaint()

    def dragLeaveEvent(self, e: QDragLeaveEvent) -> None:
        """Remove the label when its widget is dragged out."""
        if self._last_widget is not None:
            self.label_holder.remove(self._last_widget.label)
        return super().dragLeaveEvent(e)

    def set_draggable(self, draggable: bool):
        """Change draggable state of all children."""
        for widget in self.label_holder.widget_holder:
            widget.draggable = draggable

    @property
    def _widget_holder(self) -> WidgetHolder:
        """Return the holder with child widgets."""
        return self.label_holder.widget_holder

    @property
    def type(self) -> Optional[type]:
        """Return type of values stored in labels. None if no labels."""
        if not self._labels:
            return None
        return type(self._labels[0].value)
