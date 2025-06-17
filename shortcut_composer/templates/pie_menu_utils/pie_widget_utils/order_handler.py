# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterator, Callable

from ..pie_label import PieLabel
from .widget_holder import WidgetHolder


class OrderHandler:
    """
    Represents the pie icons as a positional label container.

    Creates and controls the publicly available WidgetHolder with
    actual pie widgets. Is responsible for making sure that WidgetHolder
    state always reflect the internal state of this container.
    """

    def __init__(
        self,
        widget_holder: WidgetHolder,
        allow_value_edit_callback: Callable[[], bool],
    ) -> None:
        self._widget_holder = widget_holder
        self._allow_value_edit_callback = allow_value_edit_callback

        self._labels: list[PieLabel] = []

    # change list to tuple?
    @property
    def labels(self) -> list[PieLabel]:
        return self._labels.copy()

    def replace_labels(self, labels: list[PieLabel]) -> None:
        self._labels = labels.copy()
        self._widget_holder.reset(self._labels)

    def append(self, label: PieLabel) -> None:
        """Append the new label to the holder."""
        if self._allow_value_edit_callback():
            self._labels.append(label)
            self._widget_holder.reset(self._labels)

    def insert(self, index: int, label: PieLabel) -> None:
        """Insert the new label to the holder at given index."""
        if self._allow_value_edit_callback():
            self._labels.insert(index, label)
            self._widget_holder.reset(self._labels)

    def remove(self, label: PieLabel) -> None:
        """Remove the label from the holder."""
        if label in self._labels and self._allow_value_edit_callback():
            self._labels.remove(label)
            self._widget_holder.reset(self._labels)

    def index(self, label: PieLabel) -> int:
        """Return the index at which the label is stored."""
        return self._labels.index(label)

    def swap(self, _a: PieLabel, _b: PieLabel, /) -> None:
        """TODO: swap without removing widgets is faster and does not blink"""

        idx_a = self._labels.index(_a)
        idx_b = self._labels.index(_b)

        self._labels[idx_b] = _a
        self._labels[idx_a] = _b

        widget_a = self._widget_holder.on_label(self._labels[idx_a])
        widget_b = self._widget_holder.on_label(self._labels[idx_b])

        self._widget_holder.swap(widget_a, widget_b)

    def __iter__(self) -> Iterator[PieLabel]:
        """Iterate over all labels in the holder."""
        return iter(self._labels)

    def __bool__(self) -> bool:
        """Return whether the label list is empty."""
        return bool(self._labels)
