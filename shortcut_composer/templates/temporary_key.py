# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from core_components import Controller, Instruction
from .raw_instructions import RawInstructions

T = TypeVar('T')


class TemporaryKey(RawInstructions, Generic[T]):
    """
    Temporarily activate (long press) a value or toggle it (short press).

    Action switches between two states: `low_value` and `high_value`.
    - pressing a key ensures `high_state`
    - releasing a key before `time_interval` toggles between states
    - releasing a key after `time_interval` ensures `low_state`

    ### Arguments:

    - `name`         -- unique name of action. Must match the definition
                        in shortcut_composer.action file.
    - `controller`   -- defines which krita property will be modified.
    - `high_value`   -- value to switch to compatible with controller.
    - `low_value`    -- (optional*) value to return to compatible with
                        controller. If not given, taken from controller.
    - `instructions` -- (optional) list of additional instructions to
                        perform on key press and release.
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long.

    *some controllers don't have a default value. Then providing it
     becomes required.

    ### Action implementation example:

    Example action is meant to toggle between opacity 100% and 50%.
    Using `OpacityController` which is one of the available `controllers`
    tells krita, that requested values relate to brush opacity.

    Key press shorter than 0.3 seconds will toggle between 100% and 50%
    brush opacity. Longer press will ensure 50%, which will go back to
    100% on the key release.

    ```python
    templates.TemporaryKey(
        name="Change opacity between 100 and 50,
        controller=controllers.OpacityController(),
        high_value=50,
        low_value=100,
        instructions=[], # See "instructions" for more info
        short_vs_long_press_time=0.3,
    )
    ```
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        high_value: T,
        low_value: T | None = None,
        instructions: list[Instruction] | None = None,
        short_vs_long_press_time: float | None = None
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)
        self._controller = controller
        self._high_value = high_value
        self._low_value = self._read_default_value(low_value)
        self._was_high_before_press = False

    def _set_low(self) -> None:
        """Switch to low state."""
        self._controller.set_value(self._low_value)

    def _set_high(self) -> None:
        """Switch to high state."""
        self._controller.set_value(self._high_value)

    def _is_high_state(self) -> bool:
        """Defines how to determine that current state is high."""
        return self._controller.get_value() == self._high_value

    def on_key_press(self) -> None:
        """Set high state only if state before press was low."""
        self._controller.refresh()
        super().on_key_press()
        self._was_high_before_press = self._is_high_state()
        if not self._was_high_before_press:
            self._set_high()

    def on_short_key_release(self) -> None:
        """Set low state only when going from high state."""
        super().on_short_key_release()
        if self._was_high_before_press:
            self._set_low()

    def on_long_key_release(self) -> None:
        """End of long press ensures low state."""
        super().on_long_key_release()
        self._set_low()

    def _read_default_value(self, value: T | None) -> T:
        """Read value from controller if it was not given."""
        if (default := self._controller.DEFAULT_VALUE) is None:
            raise ValueError(
                f"{self._controller} can't be used with TemporaryKeys.")
        return value if value is not None else default
