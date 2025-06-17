# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterator

from api_krita.pyqt import BaseWidget
from composer_utils import CirclePoints
from composer_utils.label import LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget

from ..pie_label import PieLabel
from ..pie_config import PieConfig
from ..pie_style_holder import PieStyleHolder

PieLabelWidget = LabelWidget[PieLabel]


class WidgetHolder:
    """Holds LabelWidgets in relation to their angles on PieWidget."""

    def __init__(
        self,
        config: PieConfig,
        style_holder: PieStyleHolder,
        owner: BaseWidget,
    ) -> None:
        self._config = config
        self._style_holder = style_holder
        self._owner = owner

        self._widgets: dict[int, PieLabelWidget] = {}

    def reset(
        self,
        labels: list[PieLabel],
    ) -> None:
        """
        Ensure the icon widgets properly represents this container.
        """
        # values need to be saved for labels to scale properly
        self._style_holder.pie_style.amount_of_labels = len(labels)

        children_widgets: list[LabelWidget[PieLabel]] = []
        for label in labels:
            children_widgets.append(dispatch_label_widget(label)(
                label, self._style_holder.label_style, self._owner))

        circle_points = CirclePoints(
            center=self._owner.center,
            radius=self._style_holder.pie_style.pie_radius)
        angles = circle_points.iterate_over_circle(len(labels))

        for child in self:
            child.setParent(None)  # type: ignore
        self._widgets = {}

        for child, (angle, point) in zip(children_widgets, angles):
            child.label.angle = angle
            child.label.center = point
            child.draggable = True
            child.setParent(self._owner)
            self._add(child)
            child.show()

    def swap(self, w_a: PieLabelWidget, w_b: PieLabelWidget, /) -> None:
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

        closest = min(self._angles(), key=angle_difference)
        return self._widgets[closest]

    def on_label(self, label: PieLabel) -> PieLabelWidget:
        """Return widget wrapping the label of the same value as given."""
        for widget in self._widgets.values():
            if widget.label == label:
                return widget
        raise ValueError(f"{label} not in holder.")

    def clear_forced_widgets(self) -> None:
        """Clear the forced colors of all held widgets. Helper method."""
        for widget in self._widgets.values():
            widget.forced = False

    def _add(self, widget: PieLabelWidget) -> None:
        """Add a new LabelWidget[Label] to the holder."""
        self._widgets[widget.label.angle] = widget
        widget.move_center(widget.label.center)

    # Other name?
    def _angles(self) -> Iterator[int]:
        """Iterate over all angles at which LabelWidgets are."""
        return iter(self._widgets.keys())

    def __iter__(self) -> Iterator[PieLabelWidget]:
        """Iterate over all held LabelWidgets."""
        for angle in sorted(self._angles()):
            yield self._widgets[angle]

    def __len__(self) -> int:
        """Return amount of held LabelWidgets."""
        return len(self._widgets)
