# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPaintEvent, QDragMoveEvent, QDragEnterEvent

from api_krita.pyqt import Painter, AnimatedWidget
from .pie_style import PieStyle
from .label_holder import LabelHolder
from .pie_painter import PiePainter
from .label_widgets import LabelWidget, create_label_widget
from .circle_points import CirclePoints


from composer_utils import Config


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

    def __init__(
        self,
        style: PieStyle,
        labels: LabelHolder,
        parent=None
    ):
        super().__init__(parent, Config.PIE_ANIMATION_TIME.read())

        self._style = style
        self.labels = labels
        self._label_widgets = self._create_label_widgets()
        self._circle_points: CirclePoints

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Popup |
            Qt.FramelessWindowHint |
            Qt.NoDropShadowWindowHint))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CrossCursor)

        size = self._style.widget_radius*2
        self.setGeometry(0, 0, size, size)

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

    def move_center(self, new_center: QPoint) -> None:
        """Move the widget by providing a new center point."""
        self.move(new_center-self._center)  # type: ignore

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            PiePainter(painter, self.labels, self._style)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
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
        label = self.labels.from_angle(round(angle))
        if label == source_widget.label:
            return e.accept()

        self.labels.swap(label, source_widget.label)
        for widget in self._label_widgets:
            widget.move_to_label()

        self.repaint()
        e.accept()

    def _create_label_widgets(self) -> List[LabelWidget]:
        """Create LabelWidgets that represent the labels."""
        childred: List[LabelWidget] = []
        for label in self.labels:
            label_widget = create_label_widget(label, self._style, self)
            label_widget.move_to_label()
            childred.append(label_widget)
        return childred
