# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Iterator
from ..label_widget import LabelWidget
from ..label import Label


class WidgetHolder:
    """Holds LabelWidgets in relation to their angles on PieWidget."""

    def __init__(self):
        self._widgets: Dict[int, LabelWidget] = {}

    def add(self, widget: LabelWidget) -> None:
        """Add a new LabelWidget to the holder."""
        self._widgets[widget.label.angle] = widget

    def on_angle(self, angle: float) -> LabelWidget:
        """Return LabelWidget which is the closest to given `angle`."""
        def angle_difference(label_angle: float) -> float:
            """Return the smallest difference between two angles."""
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self.angles(), key=angle_difference)
        return self._widgets[closest]

    def on_label(self, label: Label):
        """Return widget wrapping the label of the same value as given."""
        for widget in self._widgets.values():
            if widget.label == label:
                return widget
        raise ValueError(f"{label} not in holder.")

    def angle(self, widget: LabelWidget) -> int:
        """Return at which angle is the given LabelWidget."""
        for angle, held_widget in self._widgets.items():
            if widget == held_widget:
                return angle
        raise ValueError(f"{widget} not in holder.")

    def clear(self):
        """Remove all widgets from the holder."""
        self._widgets = {}

    def angles(self) -> Iterator[int]:
        """Iterate over all angles at which LabelWidgets are."""
        return iter(self._widgets.keys())

    def __iter__(self) -> Iterator[LabelWidget]:
        """Iterate over all held LabelWidgets."""
        for angle in sorted(self.angles()):
            yield self._widgets[angle]

    def __len__(self) -> int:
        """Return amount of held LabelWidgets."""
        return len(self._widgets)
