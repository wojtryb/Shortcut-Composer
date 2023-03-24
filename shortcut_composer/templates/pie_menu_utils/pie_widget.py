# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, TypeVar, Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QPaintEvent)

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils.config import Config
from .pie_style import PieStyle
from .label import Label
from .label_widget import LabelWidget
from .label_widget_utils import create_label_widget
from .pie_config import PieConfig
from .widget_utils import (
    WidgetHolder,
    CirclePoints,
    PiePainter)

T = TypeVar('T')


class PieWidget(AnimatedWidget, BaseWidget):
    """
    PyQt5 widget with icons on ring that can be selected by hovering.

    Methods inherits from QWidget used by other components:
    - show() - displays the widget
    - hide() - hides the widget
    - repaint() - updates widget display after its data was changed

    Contains children widgets that are draggable. When one of the
    children is dragged, the widget enters the edit mode. That can be
    used by whoever controls this widget to handle it differently.

    Stores the values in three forms:
    - Labels: contain bare data
    - LabelWidgets: widget children displaying a single Label
    - LabelHolder: container of all LabelWidgets that operate on angles

    Makes changes to LabelHolder when one of children is dragged.
    When the widget is hidden while in the edit mode, changes made to
    the LabelHolder are saved in the related configuration.
    """

    def __init__(
        self,
        style: PieStyle,
        labels: List[Label],
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
            Qt.NoDropShadowWindowHint))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CrossCursor)

        self._style = style
        self._labels = labels
        self.config = config

        self.active: Optional[Label] = None
        self.is_edit_mode = False
        self._last_widget = None

        self._circle_points = CirclePoints(
            center=self.center,
            radius=self._style.pie_radius)

        self.aggregator = ChildAggregator(
            self._labels,
            self._style,
            self._circle_points,
            self)

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._style.deadzone_radius

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            PiePainter(painter, self._labels, self._style, self.is_edit_mode)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Start edit mode when one of the draggable children gets dragged."""
        e.accept()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """Swap children during drag when mouse is moved to another zone."""
        e.accept()
        source_widget = e.source()
        pos = e.pos()
        distance = self._circle_points.distance(pos)
        if not isinstance(source_widget, LabelWidget):
            return

        self._last_widget = source_widget
        if distance > self._style.widget_radius:
            return self.aggregator.remove(source_widget.label)
        if distance < self._style.deadzone_radius:
            return

        if source_widget.label not in self.aggregator:
            return self.aggregator.append(source_widget.label)

        _a = self.aggregator.widget_holder.on_label(source_widget.label)
        angle = self._circle_points.angle_from_point(pos)
        _b = self.aggregator.widget_holder.on_angle(angle)
        if _a != _b:
            self.aggregator.swap(_a.label, _b.label)
            self.repaint()

    def dragLeaveEvent(self, e: QDragLeaveEvent) -> None:
        if self._last_widget is not None:
            self.aggregator.remove(self._last_widget.label)
        return super().dragLeaveEvent(e)

    def show(self):
        self.set_draggable(False)
        return super().show()

    def set_draggable(self, draggable: bool):
        for widget in self.aggregator.widgets():
            widget.draggable = draggable


class ChildAggregator:
    def __init__(
        self,
        labels: List[Label],
        style: PieStyle,
        circle_points: CirclePoints,
        owner: QWidget,
    ) -> None:
        self._labels = labels
        self._style = style
        self._circle_points = circle_points
        self._owner = owner

        self.widget_holder: WidgetHolder = WidgetHolder()
        self._reset()

    def append(self, label: Label):
        self._labels.append(label)
        self._reset()

    def remove(self, label: Label):
        if label in self._labels:
            self._labels.remove(label)
            self._reset()

    def swap(self, _a: Label, _b: Label):
        _a.swap_locations(_b)

        idx_a, idx_b = self._labels.index(_a), self._labels.index(_b)
        self._labels[idx_b] = _a
        self._labels[idx_a] = _b

        self._reset()

    def __iter__(self):
        return iter(self._labels)

    def __bool__(self):
        return bool(self._labels)

    def widgets(self):
        return iter(self.widget_holder)

    def _reset(self) -> None:
        for child in self.widget_holder:
            child.setParent(None)  # type: ignore
        self.widget_holder.clear()

        children_widgets: List[LabelWidget] = []
        for label in self._labels:
            children_widgets.append(
                create_label_widget(label, self._style, self._owner))

        angle_iterator = self._circle_points.iterate_over_circle(
            len(children_widgets))
        for child, (angle, point) in zip(children_widgets, angle_iterator):
            child.setParent(self._owner)
            child.show()
            child.label.angle = angle
            child.label.center = point
            child.move_to_label()
            self.widget_holder.add(child)
