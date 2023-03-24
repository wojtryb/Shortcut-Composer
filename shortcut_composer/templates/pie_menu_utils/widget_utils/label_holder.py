# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from PyQt5.QtWidgets import QWidget

from ..pie_style import PieStyle
from ..label import Label
from ..label_widget import LabelWidget
from ..label_widget_utils import create_label_widget
from .widget_holder import WidgetHolder
from .circle_points import CirclePoints


class LabelHolder:
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

        angles = self._circle_points.iterate_over_circle(len(self._labels))
        for child, (angle, point) in zip(children_widgets, angles):
            child.setParent(self._owner)
            child.show()
            child.label.angle = angle
            child.label.center = point
            child.move_to_label()
            self.widget_holder.add(child)
