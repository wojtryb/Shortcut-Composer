# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Iterator, Optional
from ..label_widget import LabelWidget


class WidgetHolder:
    """
    Holds LabelWidgets and in relation to their angles on PieWidget.

    Holds which of them is active (One of them None), but does not
    handle this attribute by itself - this is done by PieManager.
    """

    def __init__(self):
        self._widgets: Dict[int, LabelWidget] = {}
        self.active: Optional[LabelWidget] = None

    def add(self, widget: LabelWidget) -> None:
        """Add a new LabelWidget to the holder."""
        self._widgets[widget.label.angle] = widget

    def angles(self) -> Iterator[int]:
        """Iterate over all angles at which LabelWidgets are."""
        return iter(self._widgets.keys())

    def on_angle(self, angle: float) -> LabelWidget:
        """Return LabelWidget which is the closest to given `angle`."""

        def angle_difference(label_angle: float) -> float:
            """Return the smallest difference between two angles."""
            nonlocal angle
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self.angles(), key=angle_difference)
        return self._widgets[closest]

    def angle(self, widget: LabelWidget) -> int:
        """Return at which angle angle is the given LabelWidget."""
        for angle, held_widget in self._widgets.items():
            if widget == held_widget:
                return angle
        raise ValueError(f"{widget} not in holder.")

    def swap(self, _a: LabelWidget, _b: LabelWidget) -> None:
        """Swap two LabelWidgets that are already in the holder."""
        _a.label.swap_locations(_b.label)
        key_a, key_b = self.angle(_a), self.angle(_b)
        self._widgets[key_a], self._widgets[key_b] = _b, _a
        _a.move_to_label()
        _b.move_to_label()

    def flush(self):
        self._widgets = {}
        self.active = None

    def __iter__(self) -> Iterator[LabelWidget]:
        """Iterate over all held LabelWidgets."""
        for angle in sorted(self.angles()):
            yield self._widgets[angle]

    def __len__(self) -> int:
        """Return amount of held LabelWidgets."""
        return len(self._widgets)
