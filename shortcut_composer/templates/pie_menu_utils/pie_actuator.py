# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from config_system import Field
from core_components import Controller
from data_components import PieDeadzoneStrategy
from .pie_label import PieLabel
from .pie_widget_utils import OrderHandler


class PieActuator:
    """
    Activates the correct labels from the Pie.

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
        controller: Controller,
        strategy_field: Field,
    ) -> None:
        self._controller = controller
        self._last_label: PieLabel | None = None
        self._labels = []

        def update_strategy() -> None:
            self._current_strategy = strategy_field.read()
        self._current_strategy: PieDeadzoneStrategy
        strategy_field.register_callback(update_strategy)
        update_strategy()

    def activate(
            self,
            active: PieLabel | None,
            labels: list[PieLabel]) -> None:
        """Activate the correct label"""
        self._labels = labels

        if active is not None:
            # Out of deadzone, label picked
            self._controller.set_value(active.value)
            self._last_label = active
            return

        # In deadzone
        if self._selected_label is not None:
            self._controller.set_value(self._selected_label.value)

    @property
    def _selected_label(self) -> PieLabel | None:
        """Return label which should be picked on deadzone."""
        if self._current_strategy == PieDeadzoneStrategy.DO_NOTHING:
            return None
        elif self._current_strategy == PieDeadzoneStrategy.PICK_TOP:
            if self._labels:
                return self._labels[0]
            return None
        elif self._current_strategy == PieDeadzoneStrategy.PICK_PREVIOUS:
            if self._last_label in self._labels:
                return self._last_label
            return None

    def mark_selected_widget(
            self,
            order_handler: OrderHandler) -> None:
        """Force color of the label that is selected for being picked."""
        self._labels = order_handler.labels
        order_handler.clear_forced_widgets()

        if self._selected_label is None:
            return

        try:
            widget = order_handler.widget_on_label(self._selected_label)
        except ValueError:
            return
        widget.forced = True
