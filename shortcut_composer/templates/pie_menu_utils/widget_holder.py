# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Iterator, Optional
from .label_widgets import LabelWidget


class WidgetHolder:
    """
    Holds Labels and allows fetching them using their angle.

    Allows one of the labels to be active, but does not handle this
    attribute by itself.

    Allows iterating over Labels (default) and over angles (angles())
    """

    def __init__(self):
        self._widgets: Dict[int, LabelWidget] = {}
        self.active: Optional[LabelWidget] = None

    def add(self, widget: LabelWidget) -> None:
        """Add a new label to the holder."""
        self._widgets[widget.label.angle] = widget

    def angles(self) -> Iterator[int]:
        """Iterate over all angles of held Labels."""
        return iter(self._widgets.keys())

    def from_angle(self, angle: int) -> LabelWidget:
        """Return Label which is the closest to given `angle`."""

        def angle_difference(label_angle: int):
            """Return the smallest difference between two angles."""
            nonlocal angle
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self.angles(), key=angle_difference)
        return self._widgets[closest]

    def at(self, widget: LabelWidget):
        return [k for k, v in self._widgets.items() if v == widget][0]

    def swap(self, _a: LabelWidget, _b: LabelWidget):
        _a.label.swap_locations(_b.label)
        key_a, key_b = self.at(_a), self.at(_b)
        self._widgets[key_a], self._widgets[key_b] = _b, _a
        _a.move_to_label()
        _b.move_to_label()

    def __iter__(self) -> Iterator[LabelWidget]:
        """Iterate over all held labels."""
        return iter(self._widgets.values())

    def __len__(self) -> int:
        """Return amount of held labels."""
        return len(self._widgets)
