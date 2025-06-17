# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Callable

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import (
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QPaintEvent)

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils import CirclePoints, Config
from composer_utils.label import LabelWidget
from .pie_label import PieLabel
from .pie_style import PieStyle
from .pie_widget_utils import OrderHandler, PiePainter, WidgetHolder

T = TypeVar('T')


class PieWidget(AnimatedWidget, BaseWidget, Generic[T]):
    """
    Custom, circular widget with LabelWidgets on the edge.

    Uses OrderHandler to store children widgets representing available
    values. When the pie enters the edit mode, its children become
    draggable.

    By dragging children, user can change their order or remove them
    by moving them out of the widget. New children can be added by
    dragging them from other widgets.
    """

    def __init__(
        self,
        pie_style: PieStyle,
        allow_value_edit_callback: Callable[[], bool],
        parent=None
    ) -> None:
        AnimatedWidget.__init__(
            self,
            animation_time_s=Config.PIE_ANIMATION_TIME.read(),
            fps_limit=Config.FPS_LIMIT.read(),
            parent=parent)

        self._pie_style = pie_style
        self._allow_value_edit_callback = allow_value_edit_callback

        self._painter = PiePainter(self._pie_style)
        self.widget_holder = WidgetHolder(self._pie_style, self)
        self.order_handler = OrderHandler(
            self.widget_holder,
            self._allow_value_edit_callback)

        self.active_label: PieLabel | None = None
        self._last_widget = None
        self._is_draggable = False

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.NoDropShadowWindowHint))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.set_draggable(False)
        self.reset_size()

    # TODO: to widget holder?
    def set_draggable(self, draggable: bool) -> None:
        """Change draggable state of all children."""
        for widget in self.widget_holder:
            widget.draggable = draggable
        self._is_draggable = draggable

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._pie_style.deadzone_radius

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as qt_painter:
            self._painter.paint(qt_painter, self.order_handler.labels)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Allow dragging the widgets while in edit mode."""
        if self._is_draggable:
            return e.accept()
        e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """Handle all children actions - order change, add and remove."""
        e.accept()
        source_widget = e.source()

        if not isinstance(source_widget, LabelWidget):
            # Drag incoming from outside the PieWidget ecosystem
            return

        label = source_widget.label
        circle_points = CirclePoints(
            center=self.center,
            radius=self._pie_style.pie_radius)
        distance = circle_points.distance(e.pos())

        if self._type and not isinstance(label.value, self._type):
            # Label type does not match the type of pie menu
            return

        self._last_widget = source_widget
        if distance > self._pie_style.widget_radius:
            # Dragged out of the PieWidget
            return self.order_handler.remove(label)

        if not self.order_handler:
            # First label dragged to empty pie
            return self.order_handler.insert(0, label)

        if distance < self.deadzone:
            # Do nothing in deadzone
            return

        angle = circle_points.angle_from_point(e.pos())
        _a = self.widget_holder.on_angle(angle)

        if label not in self.order_handler or not self.order_handler:
            # Dragged with unknown label
            index = self.order_handler.index(_a.label)
            return self.order_handler.insert(index, label)

        _b = self.widget_holder.on_label(label)
        if _a == _b:
            # Dragged over the same widget
            return

        # Dragged existing label to a new location
        self.order_handler.swap(_a.label, _b.label)
        self.repaint()

    def dragLeaveEvent(self, e: QDragLeaveEvent) -> None:
        """Remove the label when its widget is dragged out."""
        if self._last_widget is not None:
            self.order_handler.remove(self._last_widget.label)
        return super().dragLeaveEvent(e)

    @property
    def _type(self) -> type | None:
        """Return type of values stored in labels. None if no labels."""
        if not self.order_handler:
            return None
        return type(self.order_handler.labels[0].value)

    def reset_size(self) -> None:
        """Set widget geometry according to style."""
        radius = self._pie_style.widget_radius
        difference = radius - self.width()//2
        new_center = QPoint(
            self.center_global.x() - difference,
            self.center_global.y())
        self.resize(2*radius, 2*radius)
        self.move_center(new_center)
