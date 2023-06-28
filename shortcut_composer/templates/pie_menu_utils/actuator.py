from typing import Optional, List
from core_components import Controller
from config_system import Field
from .label import Label
from data_components import DeadzoneStrategy


class Actuator:
    def __init__(
        self,
        controller: Controller,
        strategy_field: Field,
        labels: List[Label]
    ) -> None:
        self._controller = controller
        self._last_label: Optional[Label] = None
        self._labels = labels

        def update_strategy():
            self._current_strategy = strategy_field.read()
        self._current_strategy: DeadzoneStrategy
        strategy_field.register_callback(update_strategy)
        update_strategy()

    def activate(self, active: Optional[Label]):
        if active is not None:
            # Out of deadzone, label picked
            self._controller.set_value(active.value)
            self._last_label = active
            return

        if self._last_label is None:
            return

        # In deadzone
        if self._current_strategy == DeadzoneStrategy.DO_NOTHING:
            pass
        elif self._current_strategy == DeadzoneStrategy.ACTIVATE_TOP:
            self._controller.set_value(self._labels[0].value)
        elif self._current_strategy == DeadzoneStrategy.ACTIVATE_PREVIOUS:
            self._controller.set_value(self._last_label.value)  # type: ignore
