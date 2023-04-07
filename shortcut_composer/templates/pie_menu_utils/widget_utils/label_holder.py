# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List
from functools import partial

from api_krita.pyqt import BaseWidget
from ..pie_style import PieStyle
from ..label import Label
from ..label_widget import LabelWidget
from ..label_widget_utils import create_label_widget
from ..pie_config import PieConfig
from .widget_holder import WidgetHolder
from .circle_points import CirclePoints


class LabelHolder:
    def __init__(
        self,
        labels: List[Label],
        style: PieStyle,
        config: PieConfig,
        owner: BaseWidget,
    ) -> None:
        self._labels = labels
        self._style = style
        self._config = config
        self._config.register_callback(partial(self._reset, False))
        self._owner = owner

        self.widget_holder: WidgetHolder = WidgetHolder()
        self._reset(False)

    def append(self, label: Label):
        self._labels.append(label)
        self._reset()

    def remove(self, label: Label):
        if (label in self._labels
                and len(self._labels) > 1
                and self._config.allow_remove):
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

    def _reset(self, notify: bool = True) -> None:
        for child in self.widget_holder:
            child.setParent(None)  # type: ignore
        self.widget_holder.clear()

        children_widgets: List[LabelWidget] = []
        for label in self._labels:
            children_widgets.append(
                create_label_widget(label, self._style, self._owner))

        circle_points = CirclePoints(
            center=self._owner.center,
            radius=self._style.pie_radius)
        angles = circle_points.iterate_over_circle(len(self._labels))
        for child, (angle, point) in zip(children_widgets, angles):
            child.setParent(self._owner)
            child.show()
            child.label.angle = angle
            child.label.center = point
            child.move_to_label()
            self.widget_holder.add(child)

        if notify:
            values = [label.value for label in self._labels]
            self._config.ORDER.write(values)
