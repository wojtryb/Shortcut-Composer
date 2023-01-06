from typing import Any, List
from itertools import cycle

from core_components import Controller, Instruction
from input_adapter import PluginAction


class MultipleAssignment(PluginAction):
    """
    Cycle multiple values (short press) or return to default (long press).

    Action cycles the values in `values_to_cycle` list:
    - short key press moves to next value in list.
    - if current value does not belong to the list, start from beginning
    - when the list is exhausted, start again
    - end of long press ensures `default value`

    ### Arguments:

    - `action_name`     -- unique name of action. Must match the definition in
                            shortcut_composer.action file
    - `controller`      -- defines which krita property will be modified
    - `values_to_cycle` -- list of values compatibile with controller to cycle
    - `default_value`   -- value to switch to after long press. Does not
                            have to belong to the list.
    - `instructions`    -- list of additional instructions to perform on
                            key press and release.
    - `time_interval`   -- time [s] that specifies if key press is short or
                            long.

    ### Action implementation example:

    Action is meant to cycle brush sizes: 5px, 10px, 20px, 50px. by
    constantly short pressing a key. Using `BrushSizeController` which
    is one of the available `controllers` tells krita, that requested
    values relate to brush size.

    Long press, changes brush size to 100px which is not a value
    available with short presses.

    ```python
    MultipleAssignment(
        action_name="Brush size (cycle)",
        controller=controllers.BrushSizeController(),
        default_value=100,
        values_to_cycle=[5, 10, 20, 50],
    )
    ```
    """

    def __init__(self, *,
                 action_name: str,
                 controller: Controller,
                 values_to_cycle: List[Any],
                 default_value: Any = None,
                 instructions: List[Instruction] = [],
                 time_interval: float = 0.3) -> None:
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
