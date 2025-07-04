# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterator, Callable, Any
from itertools import zip_longest

try:
    from PyQt5.QtCore import QPoint
except ModuleNotFoundError:
    from PyQt6.QtCore import QPoint

from api_krita.pyqt import BaseWidget
from composer_utils import CirclePoints
from composer_utils.label import LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget
from ..pie_label import PieLabel
from .pie_widget_style import PieWidgetStyle

PieLabelWidget = LabelWidget[PieLabel]
EmptyCallback = Callable[[], None]


class PieWidgetOrder:
    """
    Represents labels stored in PieWidget as a positional container.

    `PieWidgetOrder` responsibilities are:
    - synchronizing values, labels and widgets
    - providing read-only access to values, labels and widgets
    - allowing editing only with methods that guarantee synchronization

    Container interface is inspired by the list, but only used features
    were implemented.

    All methods for editing the state use labels domain.
    Remaining methods allow to get labels from other domains.
    Properties allow to get read-only state of the class in any domain.

    Each time the container state is changed, all registered callbacks
    are called.
    """

    def __init__(
        self,
        pie_style: PieWidgetStyle,
        owner: BaseWidget,
    ) -> None:
        self._pie_style = pie_style
        self._owner = owner

        self._labels: list[PieLabel] = []
        """Source of truth for the container state."""
        self._widgets: dict[int, PieLabelWidget] = {}
        """Widgets wrapping labels mapped to their angle on the pie."""
        self._on_change_callbacks: list[EmptyCallback] = []
        """Callbacks to run everytime container state changes."""

    @property
    def values(self) -> list[Any]:
        """Return list of values from stored labels in their order."""
        return [label.value for label in self._labels]

    @property
    def labels(self) -> list[PieLabel]:
        """Return list of stored labels in their order."""
        return self._labels.copy()

    @property
    def widgets(self) -> list[PieLabelWidget]:
        """Return list of stored widgets in their order."""
        return [widget for widget in self._widgets.values()]

    def replace_labels(self, labels: list[PieLabel]) -> None:
        """Replace all current labels with passed ones."""
        self._labels = labels.copy()
        self._reset_widgets(self._labels)

    def append(self, label: PieLabel) -> None:
        """Append the new label at the end."""
        self._labels.append(label)
        self._reset_widgets(self._labels)

    def insert(self, index: int, label: PieLabel) -> None:
        """Insert the new label at given index."""
        self._labels.insert(index, label)
        self._reset_widgets(self._labels)

    def remove(self, label: PieLabel) -> None:
        """Remove the label. Do nothing when it does not belong."""
        if label in self._labels:
            self._labels.remove(label)
            self._reset_widgets(self._labels)

    def swap(self, _a: PieLabel, _b: PieLabel, /) -> None:
        """Swap position of two held labels."""

        # NOTE: Current implementation does not reset the widgets for
        # performance reasons

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

    def index(self, label: PieLabel) -> int:
        """Return the index at which the label is stored."""
        return self._labels.index(label)

    def label_on_angle(self, angle: float) -> PieLabel:
        """Return label, which is the closest to given `angle`."""
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

    def register_callback_on_change(self, callback: EmptyCallback) -> None:
        """Register callback called on every change in labels."""
        self._on_change_callbacks.append(callback)

    def _reset_widgets(self, labels: list[PieLabel]) -> None:
        """Ensure the widgets properly represent stored labels."""
        # values need to be saved for labels to scale properly
        self._pie_style.amount_of_labels = len(labels)
        for callback in self._on_change_callbacks:
            callback()

        # create new widgets that will replace old ones
        new_widgets: list[LabelWidget[PieLabel]] = []
        for label in labels:
            new_widgets.append(dispatch_label_widget(label)(
                label=label,
                label_widget_style=self._pie_style.label_style,
                parent=self._owner))

        old_widgets = self._widgets.copy()
        self._widgets.clear()

        circle_points = CirclePoints(
            center=self._owner.center,
            radius=self._pie_style.pie_radius)
        angles_and_centers = circle_points.iterate_over_circle(len(labels))

        # Add new and remove widgets at the same time to minimize artifacts
        it = zip_longest(old_widgets.values(), new_widgets, angles_and_centers)
        for old_widget, new_widget, angle_and_center in it:
            if angle_and_center is not None and new_widget is not None:
                self._add_widget(new_widget, *angle_and_center)

            if old_widget is not None:
                old_widget.setParent(None)  # type: ignore

    def _add_widget(
        self,
        widget: PieLabelWidget,
        angle: int,
        center: QPoint,
    ) -> None:
        """Add a new widget to the holder."""
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
        """Return whether the label list is not empty."""
        return bool(self._labels)
