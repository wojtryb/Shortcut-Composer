# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterator

from composer_utils.label import LabelWidget
from ..pie_label import PieLabel

PieLabelWidget = LabelWidget[PieLabel]


class WidgetHolder:
    """Holds LabelWidgets in relation to their angles on PieWidget."""

    def __init__(self) -> None:
        self._widgets: dict[int, PieLabelWidget] = {}

    def add(self, widget: PieLabelWidget) -> None:
        """Add a new LabelWidget[Label] to the holder."""
        self._widgets[widget.label.angle] = widget
        widget.move_center(widget.label.center)

    def swap(self, w_a: PieLabelWidget, w_b: PieLabelWidget) -> None:
        """Swap position of two widgets."""
        a_angle = w_a.label.angle
        b_angle = w_b.label.angle

        self._widgets[a_angle] = w_b
        self._widgets[b_angle] = w_a

        w_a.label.swap_locations(w_b.label)
        w_a.move_center(w_a.label.center)
        w_b.move_center(w_b.label.center)

    def on_angle(self, angle: float) -> PieLabelWidget:
        """Return LabelWidget which is the closest to given `angle`."""
        def angle_difference(label_angle: float) -> float:
            """Return the smallest difference between two angles."""
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self.angles(), key=angle_difference)
        return self._widgets[closest]

    def on_label(self, label: PieLabel) -> PieLabelWidget:
        """Return widget wrapping the label of the same value as given."""
        for widget in self._widgets.values():
            if widget.label == label:
                return widget
        raise ValueError(f"{label} not in holder.")

    def angle(self, widget: PieLabelWidget) -> int:
        """Return at which angle is the given LabelWidget[Label]."""
        for angle, held_widget in self._widgets.items():
            if widget == held_widget:
                return angle
        raise ValueError(f"{widget} not in holder.")

    def clear(self) -> None:
        """Remove all widgets from the holder."""
        self._widgets = {}

    def angles(self) -> Iterator[int]:
        """Iterate over all angles at which LabelWidgets are."""
        return iter(self._widgets.keys())

    def __iter__(self) -> Iterator[PieLabelWidget]:
        """Iterate over all held LabelWidgets."""
        for angle in sorted(self.angles()):
            yield self._widgets[angle]

    def __len__(self) -> int:
        """Return amount of held LabelWidgets."""
        return len(self._widgets)

    def clear_forced_widgets(self) -> None:
        """Clear the forced colors of all held widgets. Helper method."""
        for widget in self._widgets.values():
            widget.forced = False
