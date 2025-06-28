# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from data_components import PieDeadzoneStrategy
from .pie_widget import PieWidget
from .pie_widget_utils import PieWidgetLabel


class PieActuator:
    """
    Activates the correct labels from the Pie.

    TODO update dosctring and class name

    When a valid label is given in `activate()` method, it us activated
    and also remembered.

    When label is not given in `activate()` method, it means that user
    closed the pie while still being in deadzone.
    Then it is handled using the currently active strategy.

    Actuator tracks selected strategy using `strategy_field` passed on
    initialization. It can be changed in runtime.
    """

    def __init__(
        self,
        pie_widget: PieWidget,
        initial_label: PieWidgetLabel | None = None,
        initial_strategy: PieDeadzoneStrategy = PieDeadzoneStrategy.DO_NOTHING,
    ) -> None:
        self._pie_widget = pie_widget
        self._previous_label = initial_label
        self.strategy = initial_strategy

    def select(self) -> PieWidgetLabel | None:
        active = self._pie_widget.active_label

        # Out of deadzone, label picked
        if active is not None:
            self._previous_label = active
            return active

        # In deadzone, use strategy to select label
        return self._label_from_strategy()

    def mark_suggested_widget(self) -> None:
        """Force color of the label that is selected for being picked."""
        self.unmark_all_widgets()

        label = self._label_from_strategy()
        if label is None:
            return

        if label in self._pie_widget.order_handler.labels:
            widget = self._pie_widget.order_handler.widget_with_label(label)
            widget.forced = True

    def unmark_all_widgets(self):
        for widget in self._pie_widget.order_handler.widgets:
            widget.forced = False

    def _label_from_strategy(self) -> PieWidgetLabel | None:
        """Return label suggested by current strategy."""
        labels = self._pie_widget.order_handler.labels

        match self.strategy:
            case PieDeadzoneStrategy.PICK_TOP:
                if labels:
                    return labels[0]
            case PieDeadzoneStrategy.PICK_PREVIOUS:
                if self._previous_label in labels:
                    return self._previous_label
        return None
