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
from composer_utils import Label, LabelWidget, Config
from .edit_mode import EditMode
from .pie_style import PieStyle
from .pie_config import PieConfig
from .pie_widget_utils import (
    WidgetHolder,
    CirclePoints,
    LabelHolder,
    PiePainter)

T = TypeVar('T')


class PieWidget(AnimatedWidget, BaseWidget, Generic[T]):
    """
    PyQt5 widget with icons on ring that can be selected by hovering.

    Uses LabelHolder to store children widgets representing available
    values. When the pie enters the edit mode, its children become
    draggable.

    By dragging children, user can change their order or remove them
    by moving them out of the widget. New children can be added by
    dragging them from other widgets.
    """

    def __init__(
        self,
        pie_style: PieStyle,
        labels: List[Label[T]],
        edit_mode: EditMode,
        config: PieConfig,
        parent=None
    ) -> None:
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        self.setGeometry(0, 0,
                         pie_style.widget_radius * 2,
                         pie_style.widget_radius * 2)

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

        self._pie_style = pie_style
        self._labels = labels
        self.edit_mode = edit_mode
        self.config = config

        self.config.PIE_RADIUS_SCALE.register_callback(self._reset)
        self.config.ICON_RADIUS_SCALE.register_callback(self._reset)
        Config.PIE_GLOBAL_SCALE.register_callback(self._reset)
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(self._reset)

        self.active: Optional[Label] = None
        self._last_widget = None

        self.label_holder = LabelHolder(
            labels=self._labels,
            pie_style=self._pie_style,
            config=self.config,
            owner=self)

        self.set_draggable(False)

    def _reset(self):
        """Set widget geometry according to style and refresh CirclePoints."""
        widget_diameter = self._pie_style.widget_radius*2
        self.setGeometry(0, 0, widget_diameter, widget_diameter)

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._pie_style.deadzone_radius

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            PiePainter(painter, self._labels, self._pie_style)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Allow dragging the widgets while in edit mode."""
        if self.edit_mode:
            return e.accept()
        e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """Handle all children actions - order change, add and remove."""
        e.accept()
        source_widget = e.source()
        label = source_widget.label
        circle_points = CirclePoints(
            center=self.center,
            radius=self._pie_style.pie_radius)
        distance = circle_points.distance(e.pos())

        if not isinstance(source_widget, LabelWidget):
            # Drag incoming from outside the PieWidget ecosystem
            return

        if self._type and not isinstance(label.value, self._type):
            # Label type does not match the type of pie menu
            return

        self._last_widget = source_widget
        if distance > self._pie_style.widget_radius:
            # Dragged out of the PieWidget
            return self.label_holder.remove(label)

        if not self._labels:
            # First label dragged to empty pie
            return self.label_holder.insert(0, label)

        if distance < self._pie_style.deadzone_radius:
            # Do nothing in deadzone
            return

        angle = circle_points.angle_from_point(e.pos())
        _a = self.widget_holder.on_angle(angle)

        if label not in self.label_holder or not self._labels:
            # Dragged with unknown label
            index = self.label_holder.index(_a.label)
            return self.label_holder.insert(index, label)

        _b = self.widget_holder.on_label(label)
        if _a == _b:
            # Dragged over the same widget
            return

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
    def widget_holder(self) -> WidgetHolder:
        """Return the holder with child widgets."""
        return self.label_holder.widget_holder

    @property
    def _type(self) -> Optional[type]:
        """Return type of values stored in labels. None if no labels."""
        if not self._labels:
            return None
        return type(self._labels[0].value)
