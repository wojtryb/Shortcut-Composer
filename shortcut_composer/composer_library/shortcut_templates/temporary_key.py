from typing import Any
from dataclasses import dataclass, field

from ..krita_api.controllers import Controller
from ..shortcut_connection_utils import PluginAction


@dataclass
class TemporaryKey(PluginAction):
    """
    TODO: this docstring is no longer right
    Abstract class with custom key event interface for 'temporary keys'

    Action consists of two states: low and high.
    - short key presses toggle between states
    - starting a long press ensures high state
    - ending a long press ensures low state
    """

    controller: Controller
    high_value: Any
    low_value: Any = None
    time_interval: float = 0.3
    _was_low_before_press: bool = field(init=False, default=False)

    def __post_init__(self):
        if not self.low_value:
            self.low_value = self.controller.default_value

    def _set_low(self) -> None:
        """Defines how to switch to low state."""
        self.controller.set_value(self.low_value)

    def _set_high(self) -> None:
        """Defines how to switch to high state."""
        self.controller.set_value(self.high_value)

    def _is_low_state(self) -> Any:
        """Defines how to determine that current state is high."""
        return self.controller.get_value() == self.low_value

    def on_key_press(self) -> None:
        """Set high state only if state before press was low."""
        self._was_low_before_press = self._is_low_state()
        if self._was_low_before_press:
            self._set_high()

    def on_short_key_release(self) -> None:
        """Set low state only when going from high state."""
        if self._was_low_before_press:
            self._set_low()

    def on_long_key_release(self) -> None:
        """End of long press ensures low state."""
        self._set_low()
