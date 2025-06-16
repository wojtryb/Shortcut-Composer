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
        self._locked = False

    def reset(
        self,
        labels: list[PieLabel],
        notify: bool = True
    ) -> None:
        """
        Ensure the icon widgets properly represents this container.

        If notify flag is set to True, saves the new order to config.
        """
        if self._locked:
            return
        # Reset is not needed when labels did not change from last reset
        current_labels = [widget.label for widget in self]
        # HACK: Labels need to be reset after config was changed, even
        # when the values are still the same
        if current_labels == labels and notify:
            return

        self._locked = True
        if notify:
            self._config.set_values([label.value for label in labels])
        self._locked = False

        for child in self:
            child.setParent(None)  # type: ignore
        self._clear()

        children_widgets: list[LabelWidget[PieLabel]] = []
        for label in labels:
            children_widgets.append(dispatch_label_widget(label)(
                label, self._style_holder.label_style, self._owner))

        circle_points = CirclePoints(
            center=self._owner.center,
            radius=self._style_holder.pie_style.pie_radius)
        angles = circle_points.iterate_over_circle(len(labels))
        for child, (angle, point) in zip(children_widgets, angles):
            child.setParent(self._owner)
            child.show()
            child.label.angle = angle
            child.label.center = point
            child.draggable = True
            self._add(child)

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

    def _clear(self) -> None:
        """Remove all widgets from the holder."""
        self._widgets = {}

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
