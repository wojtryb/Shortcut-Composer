from typing import Any, List

from ..components import Controller, Instruction
from ..connection_utils import PluginAction


class TemporaryKey(PluginAction):
    """
    TODO: this docstring is no longer right
    Abstract class with custom key event interface for 'temporary keys'

    Action consists of two states: low and high.
    - short key presses toggle between states
    - starting a long press ensures high state
    - ending a long press ensures low state
    """

    def __init__(self, *,
                 action_name: str,
                 time_interval: float = 0.3,
                 controller: Controller,
                 low_value: Any = None,
                 high_value: Any,
                 instructions: List[Instruction] = []) -> None:
        super().__init__(
            action_name=action_name,
            time_interval=time_interval,
            controller=controller,
            instructions=instructions)

        self.low_value = self._read_default_value(low_value)
        self.high_value = high_value
        self._was_high_before_press = False

    def _set_low(self) -> None:
        """Defines how to switch to low state."""
        self._controller.set_value(self.low_value)

    def _set_high(self) -> None:
        """Defines how to switch to high state."""
        self._controller.set_value(self.high_value)

    def _is_high_state(self) -> Any:
        """Defines how to determine that current state is high."""
        return self._controller.get_value() == self.high_value

    def on_key_press(self) -> None:
        """Set high state only if state before press was low."""
        self._instructions.enter()
        self._was_high_before_press = self._is_high_state()
        if not self._was_high_before_press:
            self._set_high()

    def on_short_key_release(self) -> None:
        """Set low state only when going from high state."""
        if self._was_high_before_press:
            self._set_low()

    def on_long_key_release(self) -> None:
        """End of long press ensures low state."""
        self._set_low()

    def on_every_key_release(self) -> None:
        self._instructions.exit()
