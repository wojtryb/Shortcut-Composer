from typing import Any
from dataclasses import dataclass

from ..api_adapter import Controller
from ..plugin_action_utils import PluginAction


@dataclass
class TemporaryAction(PluginAction):
    """
    Abstract class with custom key event interface for 'temporary keys'

    Action consists of two states: low and high.
    - short key presses toggle between states
    - starting a long press ensures high state
    - ending a long press ensures low state

    Child class has to define both states:
    - set_low
    - set_high
    - is_high_state
    """

    controller: Controller
    high_value: Any
    low_value: Any = None
    time_interval: float = 0.3

    def __post_init__(self):
        if not self.low_value:
            self.low_value = self.controller.default_value

    def _set_low(self) -> None:
        """Defines how to switch to low state."""
        self.controller.set_value(self.low_value)

    def _set_high(self) -> None:
        """Defines how to switch to high state."""
        self.controller.set_value(self.high_value)

    def _is_high_state(self) -> Any:
        """Defines how to determine that current state is high."""
        return self.controller.get_value() == self.high_value

    def on_key_press(self):
        """Set high state only if state before press was low."""
        self._state_before_press = self._is_high_state()
        if not self._state_before_press:
            self._set_high()

    def on_short_key_release(self):
        """Set low state only when going from high state."""
        if self._state_before_press:
            self._set_low()

    def on_long_key_release(self):
        """End of long press ensures low state."""
        self._set_low()
