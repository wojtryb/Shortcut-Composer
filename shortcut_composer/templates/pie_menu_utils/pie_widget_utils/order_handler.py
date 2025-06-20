# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterator, Callable
from itertools import zip_longest

from PyQt5.QtCore import QPoint

from api_krita.pyqt import BaseWidget
from composer_utils import CirclePoints
from composer_utils.label import LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget
from ..pie_label import PieLabel
from ..pie_style import PieStyle

PieLabelWidget = LabelWidget[PieLabel]
EmptyCallback = Callable[[], None]


class OrderHandler:
    """
    Represents the pie icons as a positional label container.

    Creates and controls the publicly available WidgetHolder with
    actual pie widgets. Is responsible for making sure that WidgetHolder
    state always reflect the internal state of this container.
    """

    def __init__(
        self,
        pie_style: PieStyle,
        owner: BaseWidget,
        allow_value_edit_callback: Callable[[], bool],
    ) -> None:
        self._pie_style = pie_style
        self._owner = owner
        self._allow_value_edit_callback = allow_value_edit_callback

        self._labels: list[PieLabel] = []
        self._widgets: dict[int, PieLabelWidget] = {}
        self._on_change_callbacks: list[EmptyCallback] = []

    @property
    def values(self):
        return [label.value for label in self._labels]

    @property
    def labels(self) -> list[PieLabel]:
        return self._labels.copy()

    @property
    def widgets(self) -> list[PieLabelWidget]:
        return [widget for widget in self._widgets.values()]

    def replace_labels(self, labels: list[PieLabel]) -> None:
        self._labels = labels.copy()
        self._reset_widgets(self._labels)

    def append(self, label: PieLabel) -> None:
        """Append the new label to the holder."""
        if self._allow_value_edit_callback():
            self._labels.append(label)
            self._reset_widgets(self._labels)

    def insert(self, index: int, label: PieLabel) -> None:
        """Insert the new label to the holder at given index."""
        if self._allow_value_edit_callback():
            self._labels.insert(index, label)
            self._reset_widgets(self._labels)

    def remove(self, label: PieLabel) -> None:
        """Remove the label from the holder."""
        if label in self._labels and self._allow_value_edit_callback():
            self._labels.remove(label)
            self._reset_widgets(self._labels)

    def index(self, label: PieLabel) -> int:
        """Return the index at which the label is stored."""
        return self._labels.index(label)

    def swap(self, _a: PieLabel, _b: PieLabel, /) -> None:
        """TODO: swap without removing widgets is faster and does not blink"""

        idx_a = self._labels.index(_a)
        idx_b = self._labels.index(_b)

        w_a = self.widget_with_label(self._labels[idx_a])
        w_b = self.widget_with_label(self._labels[idx_b])

        label_a = w_a.label
        label_b = w_b.label

        self._labels[idx_b] = label_a
        self._labels[idx_a] = label_b

        self._widgets[label_a.angle] = w_b
        self._widgets[label_b.angle] = w_a

        label_a.angle, label_b.angle = label_b.angle, label_a.angle
        label_a.center, label_b.center = label_b.center, label_a.center

        w_a.move_center(label_a.center)
        w_b.move_center(label_b.center)

        for callback in self._on_change_callbacks:
            callback()

    def label_on_angle(self, angle: float) -> PieLabel:
        """Return Label, which widget is the closest to given `angle`."""
        def angle_difference(label_angle: float) -> float:
            """Return the smallest difference between two angles."""
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self._angles(), key=angle_difference)
        return self._widgets[closest].label

    def widget_with_label(self, label: PieLabel) -> PieLabelWidget:
        """Return widget wrapping the label of the same value as given."""
        for widget in self._widgets.values():
            if widget.label == label:
                return widget
        raise ValueError(f"{label} not in holder.")

    def register_callback_on_change(self, callback: EmptyCallback):
        self._on_change_callbacks.append(callback)

    def _reset_widgets(
        self,
        labels: list[PieLabel],
    ) -> None:
        """
        Ensure the icon widgets properly represent this container.
        """
        # values need to be saved for labels to scale properly
        self._pie_style.amount_of_labels = len(labels)
        for callback in self._on_change_callbacks:
            callback()

        new_widgets: list[LabelWidget[PieLabel]] = []
        for label in labels:
            new_widgets.append(dispatch_label_widget(label)(
                label, self._pie_style.label_style, self._owner))

        circle_points = CirclePoints(
            center=self._owner.center,
            radius=self._pie_style.pie_radius)
        angles = circle_points.iterate_over_circle(len(labels))

        old_widgets = self._widgets.copy()
        self._widgets.clear()

        # Add new and remove widgets at the same time to minimize blinking
        iterator = zip_longest(old_widgets.values(), new_widgets, angles)
        for old_widget, new_widget, angle_and_point in iterator:
            if angle_and_point is not None and new_widget is not None:
                angle, point = angle_and_point
                self._add_widget(new_widget, angle, point)

            if old_widget is not None:
                old_widget.setParent(None)  # type: ignore

    def _add_widget(
        self,
        widget: PieLabelWidget,
        angle: int,
        center: QPoint,
    ) -> None:
        """Add a new LabelWidget[Label] to the holder."""
        widget.label.angle = angle
        widget.label.center = center
        widget.draggable = True
        widget.setParent(self._owner)
        self._widgets[widget.label.angle] = widget
        widget.move_center(widget.label.center)
        widget.show()

    def _angles(self) -> Iterator[int]:
        """Iterate over all angles at which LabelWidgets are."""
        return iter(self._widgets.keys())

    def __iter__(self) -> Iterator[PieLabel]:
        """Iterate over all labels in the holder."""
        return iter(self._labels)

    def __bool__(self) -> bool:
        """Return whether the label list is empty."""
        return bool(self._labels)
