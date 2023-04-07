# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
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
    """
    Represents the pie icons as a positional label container.

    Creates and controls the publically available WidgetHolder with
    actual pie widgets. Is responsible for making sure that WidgetHolder
    state always reflect the internal state of this container.
    """

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
        # Refresh itself when config changed, but do not notify change
        # in config as holder was not their cause
        self._config.register_callback(partial(self.reset, notify=False))
        self._owner = owner

        self.widget_holder = WidgetHolder()
        self.reset(notify=False)

    def append(self, label: Label):
        """Append the new label to the holder."""
        self._labels.append(label)
        self.reset()

    def insert(self, index: int, label: Label):
        """Insert the new label to the holder at given index."""
        self._labels.insert(index, label)
        self.reset()

    def remove(self, label: Label):
        """Remove the label from the holder."""
        if (label in self._labels
                and len(self._labels) > 1
                and self._config.ALLOW_REMOVE):
            self._labels.remove(label)
            self.reset()

    def index(self, label: Label):
        """Return the index at which the label is stored."""
        return self._labels.index(label)

    def swap(self, _a: Label, _b: Label):
        """Swap positions of two labels from the holder."""
        _a.swap_locations(_b)

        idx_a, idx_b = self._labels.index(_a), self._labels.index(_b)
        self._labels[idx_b] = _a
        self._labels[idx_a] = _b

        self.reset()

    def __iter__(self):
        """Iterate over all labels in the holder."""
        return iter(self._labels)

    def reset(self, notify: bool = True) -> None:
        """
        Ensure the icon widgets properly represet this container.

        If notify flag is set to True, saves the new order to config.

        HACK: Small changes in container should not result in complete
        widget recreation.
        """
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
            child.draggable = True
            self.widget_holder.add(child)

        if notify:
            values = [label.value for label in self._labels]
            self._config.ORDER.write(values)
