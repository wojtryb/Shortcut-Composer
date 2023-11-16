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
from composer_utils.label import LabelWidget
from .edit_mode import EditMode
from .pie_label import PieLabel
from .style_holder import StyleHolder
from .pie_config import PieConfig
from .pie_widget_utils import (
    CirclePoints,
    OrderHandler,
    PiePainter)

T = TypeVar('T')


class PieWidget(AnimatedWidget, BaseWidget, Generic[T]):
    """
    PyQt5 widget with icons on ring that can be selected by hovering.

    Uses OrderHandler to store children widgets representing available
    values. When the pie enters the edit mode, its children become
    draggable.

    By dragging children, user can change their order or remove them
    by moving them out of the widget. New children can be added by
    dragging them from other widgets.
    """

    def __init__(
        self,
        style_holder: StyleHolder,
        labels: List[PieLabel[T]],
        edit_mode: EditMode,
        config: PieConfig,
        parent=None
    ) -> None:
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        diameter = 2*style_holder.pie_style.widget_radius
        self.setGeometry(0, 0, diameter, diameter)

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

        self._style_holder = style_holder
        self._labels = labels
        self._config = config
        self._edit_mode = edit_mode

        self._config.PIE_RADIUS_SCALE.register_callback(self._reset)
        self._config.ICON_RADIUS_SCALE.register_callback(self._reset)
        Config.PIE_GLOBAL_SCALE.register_callback(self._reset)
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(self._reset)

        self.active_label: Optional[PieLabel] = None
        self._last_widget = None

        self.order_handler = OrderHandler(
            labels=self._labels,
            style_holder=self._style_holder,
            config=self._config,
            owner=self)

        self.set_draggable(False)

    def set_draggable(self, draggable: bool):
        """Change draggable state of all children."""
        for widget in self.order_handler.widget_holder:
            widget.draggable = draggable

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._style_holder.pie_style.deadzone_radius

    @property
    def is_in_edit_mode(self) -> bool:
        """Return whether the pie widget is in edit mode."""
        return self._edit_mode.get()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            PiePainter(painter, self._labels, self._style_holder.pie_style)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Allow dragging the widgets while in edit mode."""
        if self._edit_mode:
            return e.accept()
        e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """Handle all children actions - order change, add and remove."""
        e.accept()
        source_widget = e.source()
        label = source_widget.label
        circle_points = CirclePoints(
            center=self.center,
            radius=self._style_holder.pie_style.pie_radius)
        distance = circle_points.distance(e.pos())

        if not isinstance(source_widget, LabelWidget):
            # Drag incoming from outside the PieWidget ecosystem
            return

        if self._type and not isinstance(label.value, self._type):
            # Label type does not match the type of pie menu
            return

        self._last_widget = source_widget
        if distance > self._style_holder.pie_style.widget_radius:
            # Dragged out of the PieWidget
            return self.order_handler.remove(label)

        if not self._labels:
            # First label dragged to empty pie
            return self.order_handler.insert(0, label)

        if distance < self.deadzone:
            # Do nothing in deadzone
            return

        angle = circle_points.angle_from_point(e.pos())
        _a = self.order_handler.widget_holder.on_angle(angle)

        if label not in self.order_handler or not self._labels:
            # Dragged with unknown label
            index = self.order_handler.index(_a.label)
            return self.order_handler.insert(index, label)

        _b = self.order_handler.widget_holder.on_label(label)
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
    def _type(self) -> Optional[type]:
        """Return type of values stored in labels. None if no labels."""
        if not self._labels:
            return None
        return type(self._labels[0].value)

    def _reset(self):
        """Set widget geometry according to style."""
        diameter = 2*self._style_holder.pie_style.widget_radius
        self.setGeometry(0, 0, diameter, diameter)
