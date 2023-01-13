# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from PyQt5.QtGui import QDragMoveEvent, QDragEnterEvent
from PyQt5.QtCore import QPoint

from api_krita.pyqt import AnimatedWidget
from composer_utils import Config
from .label_holder import LabelHolder

from .label_widgets import LabelWidget, create_label_widget
from .circle_points import CirclePoints
from .pie_style import PieStyle


class DragWidget(AnimatedWidget):
    def __init__(
        self,
        labels: LabelHolder,
        style: PieStyle,
        parent=None
    ):
        super().__init__(parent, Config.PIE_ANIMATION_TIME.read())
        self.labels = labels
        self._style = style
        self.setAcceptDrops(True)
        self._label_widgets = self._create_label_widgets()
        for label_widget in self._label_widgets:
            label_widget.move_to_label()

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        center = QPoint(self._style.widget_radius, self._style.widget_radius)
        self._circle_points = CirclePoints(
            center=center,
            radius=self._style.pie_radius
        )
        e.accept()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        pos = e.pos()
        source_widget: LabelWidget = e.source()  # type: ignore

        if self._circle_points.distance(pos) < self._style.deadzone_radius:
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
        return [create_label_widget(label, self._style, self)
                for label in self.labels]
