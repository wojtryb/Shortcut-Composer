# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterator, Callable

from api_krita.pyqt import BaseWidget
from composer_utils import CirclePoints
from composer_utils.label import LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget
from ..pie_label import PieLabel
from ..pie_style import PieStyle

PieLabelWidget = LabelWidget[PieLabel]


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

    # TODO: change list to tuple?
    @property
    def labels(self) -> list[PieLabel]:
        return self._labels.copy()

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

        self._labels[idx_b] = _a
        self._labels[idx_a] = _b

        w_a = self.widget_on_label(self._labels[idx_a])
        w_b = self.widget_on_label(self._labels[idx_b])

        # =============== #

        a_angle = w_a.label.angle
        b_angle = w_b.label.angle

        self._widgets[a_angle] = w_b
        self._widgets[b_angle] = w_a

        w_a.label.swap_locations(w_b.label)
        w_a.move_center(w_a.label.center)
        w_b.move_center(w_b.label.center)

    def label_on_angle(self, angle: float) -> PieLabel:
        """Return Label, which widget is the closest to given `angle`."""
        def angle_difference(label_angle: float) -> float:
            """Return the smallest difference between two angles."""
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self._angles(), key=angle_difference)
        return self._widgets[closest].label

    def widget_on_label(self, label: PieLabel) -> PieLabelWidget:
        """Return widget wrapping the label of the same value as given."""
        for widget in self._widgets.values():
            if widget.label == label:
                return widget
        raise ValueError(f"{label} not in holder.")

    def clear_forced_widgets(self) -> None:
        """Clear the forced colors of all held widgets. Helper method."""
        for widget in self._widgets.values():
            widget.forced = False

    def _reset_widgets(
        self,
        labels: list[PieLabel],
    ) -> None:
        """
        Ensure the icon widgets properly represents this container.
        """
        # values need to be saved for labels to scale properly
        self._pie_style.amount_of_labels = len(labels)

        new_widgets: list[LabelWidget[PieLabel]] = []
        for label in labels:
            new_widgets.append(dispatch_label_widget(label)(
                label, self._pie_style.label_style, self._owner))

        circle_points = CirclePoints(
            center=self._owner.center,
            radius=self._pie_style.pie_radius)
        angles = circle_points.iterate_over_circle(len(labels))

        for child in self._widgets.values():
            child.setParent(None)  # type: ignore
        self._widgets = {}

        for child, (angle, point) in zip(new_widgets, angles):
            child.label.angle = angle
            child.label.center = point
            child.draggable = True
            child.setParent(self._owner)
            self._add_widget(child)
            child.show()

    def _add_widget(self, widget: PieLabelWidget) -> None:
        """Add a new LabelWidget[Label] to the holder."""
        self._widgets[widget.label.angle] = widget
        widget.move_center(widget.label.center)

    def _angles(self) -> Iterator[int]:
        """Iterate over all angles at which LabelWidgets are."""
        return iter(self._widgets.keys())

    def __iter__(self) -> Iterator[PieLabel]:
        """Iterate over all labels in the holder."""
        return iter(self._labels)

    def __bool__(self) -> bool:
        """Return whether the label list is empty."""
        return bool(self._labels)
