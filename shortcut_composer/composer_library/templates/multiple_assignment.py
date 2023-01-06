from typing import Any, List
from itertools import cycle

from ..components import Controller, Instruction
from ..connection_utils import PluginAction


class MultipleAssignment(PluginAction):
    """
    Abstract class with custom key event interface for cyclic actions

    Action cycles around passed 'values_to_cycle':

    - before the cycle starts, long press works as 'temporary key'
    - then, short key press moves to next value.
    - end of long press moves to passed 'default value'

    Child class has to define how to set and determine value:
    - set_value
    - get_current_value
    """

    def __init__(self, *,
                 action_name: str,
                 time_interval: float = 0.3,
                 controller: Controller,
                 values_to_cycle: List[Any],
                 default_value: Any = None,
                 instructions: List[Instruction] = []) -> None:
        super().__init__(
            action_name=action_name,
            time_interval=time_interval,
            controller=controller,
            instructions=instructions)

        self.values_to_cycle = values_to_cycle
        self.default_value = self._read_default_value(default_value)

        self._last_value = None
        self._iterator = None

    def on_key_press(self) -> None:
        """Use key press event only for switching to first value."""
        self._instructions.enter()
        current_value = self._controller.get_value()
        if current_value != self._last_value:
            self._reset_iterator()
        self._set_value(next(self._iterator))

    def on_long_key_release(self) -> None:
        """All long releases set default value."""
        self._set_value(self.default_value)
        self._reset_iterator()

    def on_every_key_release(self) -> None:
        self._instructions.exit()

    def _set_value(self, value: Any) -> None:
        self._last_value = value
        self._controller.set_value(value)

    def _reset_iterator(self) -> None:
        self._iterator = cycle(self.values_to_cycle)
