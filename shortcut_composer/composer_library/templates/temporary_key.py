from typing import Any, List

from ..components import Controller, Instruction
from ..connection_utils import PluginAction


class TemporaryKey(PluginAction):
    """
    Action template for temporary activation (long press) or toggling (short).

    Action switches between two states: `low_value` and `high_value`.
    - pressing a key ensures `high_state`
    - releasing a key before `time_interval` toggles between states
    - releasing a key after `time_interval` ensures `low_state`

    ### Arguments:

    - `action_name`   -- unique name of action. Must match the
                          definition in shortcut_composer.action file
    - `controller`    -- defines which krita property will be modified
    - `low_value`     -- value compatibile with controller
    - `high_value`    -- value compatibile with controller
    - `instructions`  -- list of additional instructions to perform on
                          key press and release.
    - `time_interval` -- time [s] that specifies if key press is short
                          or long.

    ### Action implementation example:

    Example action is meant to toggle between opacity 100% and 50%.
    Using `OpacityController` which is one of the available `controllers`
    tells krita, that requested values relate to brush opacity.

    Key press shorter than 0.3 seconds will toggle between 100% and 50%
    brush opacity. Longer press will ensure 50%, which will go back to
    100% on the key release.

    ```python
    TemporaryKey(
        action_name="Change opacity between 100 and 50,
        controller=controllers.OpacityController(),
        low_value=100,
        high_value=50,
        instructions=[], # See instruction for more info
        time_interval=0.3,
    )
    ```
    """

    def __init__(self, *,
                 action_name: str,
                 controller: Controller,
                 low_value: Any = None,
                 high_value: Any,
                 instructions: List[Instruction] = [],
                 time_interval: float = 0.3) -> None:
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
        """End the additional instructions on every key release."""
        self._instructions.exit()
