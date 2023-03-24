# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Optional

from PyQt5.QtCore import Qt
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
from .pie_config import PieConfig
from .widget_utils import (
    NotifyingList,
    CirclePoints,
    LabelHolder,
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
        labels: NotifyingList,
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
        self._style.register_callback(self._reset)
        self._labels = labels
        self.config = config

        self.active: Optional[Label] = None
        self.is_edit_mode = False
        self._last_widget = None

        self.label_holder = LabelHolder(
            self._labels,
            self._style,
            self.config.allow_remove,
            self)
        self._circle_points: CirclePoints
        self._reset()

    def _reset(self):
        radius = self._style.widget_radius*2
        self.setGeometry(0, 0, radius, radius)
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
            return self.label_holder.remove(source_widget.label)
        if distance < self._style.deadzone_radius:
            return

        if source_widget.label not in self.label_holder or not self._labels:
            return self.label_holder.append(source_widget.label)

        _a = self.label_holder.widget_holder.on_label(source_widget.label)
        angle = self._circle_points.angle_from_point(pos)
        _b = self.label_holder.widget_holder.on_angle(angle)
        if _a != _b:
            self.label_holder.swap(_a.label, _b.label)
            self.repaint()

    def dragLeaveEvent(self, e: QDragLeaveEvent) -> None:
        if self._last_widget is not None:
            self.label_holder.remove(self._last_widget.label)
        return super().dragLeaveEvent(e)

    def show(self):
        self.set_draggable(False)
        return super().show()

    def set_draggable(self, draggable: bool):
        for widget in self.label_holder.widget_holder:
            widget.draggable = draggable
