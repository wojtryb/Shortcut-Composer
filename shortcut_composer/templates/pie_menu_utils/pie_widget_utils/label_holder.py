# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List
from functools import partial

from api_krita.pyqt import BaseWidget
from ..pie_style import PieStyle
from ..label import Label
from ..label_widget import LabelWidget
from ..label_widget_impl import dispatch_label_widget
from ..pie_config import PieConfig
from .widget_holder import WidgetHolder
from .circle_points import CirclePoints


class LabelHolder:
    """
    Represents the pie icons as a positional label container.

    Creates and controls the publicly available WidgetHolder with
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
        self._locked = False

        self.widget_holder = WidgetHolder()
        self.reset(notify=False)

    def append(self, label: Label):
        """Append the new label to the holder."""
        if (self._config.allow_value_edit):
            self._labels.append(label)
            self.reset()

    def insert(self, index: int, label: Label):
        """Insert the new label to the holder at given index."""
        if (self._config.allow_value_edit):
            self._labels.insert(index, label)
            self.reset()

    def remove(self, label: Label):
        """Remove the label from the holder."""
        if (label in self._labels and self._config.allow_value_edit):
            self._labels.remove(label)
            self.reset()

    def index(self, label: Label):
        """Return the index at which the label is stored."""
        return self._labels.index(label)

    def swap(self, _a: Label, _b: Label):
        """
        Swap positions of two labels from the holder.

        As this operation only changes label order, fully resetting all
        the widgets is not needed.
        """
        if self._locked:
            return

        idx_a = self._labels.index(_a)
        idx_b = self._labels.index(_b)

        self._labels[idx_b] = _a
        self._labels[idx_a] = _b

        widget_a = self.widget_holder.on_label(self._labels[idx_a])
        widget_b = self.widget_holder.on_label(self._labels[idx_b])

        self.widget_holder.swap(widget_a, widget_b)

        self._locked = True
        self._config.set_values([label.value for label in self._labels])
        self._locked = False

    def __iter__(self):
        """Iterate over all labels in the holder."""
        return iter(self._labels)

    def reset(self, notify: bool = True) -> None:
        """
        Ensure the icon widgets properly represents this container.

        If notify flag is set to True, saves the new order to config.
        """
        if self._locked:
            return
        # Reset is not needed when labels did not change from last reset
        current_labels = [widget.label for widget in self.widget_holder]
        # HACK: Labels need to be reset after config was changed, even
        # when the values are still the same
        if current_labels == self._labels and notify:
            return

        for child in self.widget_holder:
            child.setParent(None)  # type: ignore
        self.widget_holder.clear()

        children_widgets: List[LabelWidget] = []
        for label in self._labels:
            children_widgets.append(dispatch_label_widget(label)(
                label, self._style, self._owner))

        circle_points = CirclePoints(
            center=self._owner.center,
            radius=self._style.pie_radius)
        angles = circle_points.iterate_over_circle(len(self._labels))
        for child, (angle, point) in zip(children_widgets, angles):
            child.setParent(self._owner)
            child.show()
            child.label.angle = angle
            child.label.center = point
            child.draggable = True
            self.widget_holder.add(child)

        self._locked = True
        if notify:
            self._config.set_values([label.value for label in self._labels])
        self._locked = False
