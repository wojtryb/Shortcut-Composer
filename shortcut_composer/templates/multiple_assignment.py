# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from core_components import Controller, Instruction
from config_system import Field
from .raw_instructions import RawInstructions
from .multiple_assignment_utils import SettingsHandler

T = TypeVar('T')


class MultipleAssignment(RawInstructions, Generic[T]):
    """
    Cycle multiple values (short press) or return to default (long press).

    Action cycles the values in `values_to_cycle` list:
    - short key press moves to next value in list.
    - if current value does not belong to the list, start from beginning
    - when the list is exhausted, start from beginning
    - end of long press ensures `default value`

    ### Arguments:

    - `name`          -- unique name of action. Must match the
                         definition in shortcut_composer.action file
    - `controller`    -- defines which krita property will be modified
    - `values`        -- list of values to cycle compatible with controller
    - `default_value` -- (optional*) value to switch to after long press.
                         Does not have to belong to the list. If not
                         given, taken from a controller.
    - `instructions`  -- (optional) list of additional instructions to
                         perform on key press and release.
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long.

    *some controllers don't have a default value. Then providing it
     becomes required.

    ### Action implementation example:

    Action is meant to cycle brush sizes: 5px, 10px, 20px, 50px. by
    constantly short pressing a key. Using `BrushSizeController` which
    is one of the available `controllers` tells krita, that requested
    values relate to brush size.

    Key press longer than 0.3 seconds, changes brush size to 100px which
     is not a value available to get with shorter presses.

    ```python
    templates.MultipleAssignment(
        name="Brush size (cycle)",
        controller=controllers.BrushSizeController(),
        default_value=100,
        values=[5, 10, 20, 50],
        short_vs_long_press_time=0.3
    )
    ```
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        values: list[T],
        default_value: T | None = None,
        instructions: list[Instruction] | None = None,
        short_vs_long_press_time: float | None = None
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)

        self._controller = controller

        self._config = Field(
            config_group=f"ShortcutComposer: {self.name}",
            name="Values",
            default=values)
        self._config.register_callback(self._reset_values_to_cycle)

        self._settings = SettingsHandler(
            self.name,
            self._config,
            self._instructions)

        self._default_value = self._read_default_value(default_value)
        self._values_to_cycle: list[T]
        self._reset_values_to_cycle()

    def on_key_press(self) -> None:
        """Switch to the next value or start over when value is not in list."""
        super().on_key_press()

        if not self._values_to_cycle:
            return

        self._controller.refresh()
        current = self._controller.get_value()

        if current in self._values_to_cycle:
            id = self._values_to_cycle.index(current) + 1
            self._controller.set_value(self._values_to_cycle[id])
        else:
            self._controller.set_value(self._values_to_cycle[0])

    def on_long_key_release(self) -> None:
        """Set default value."""
        super().on_long_key_release()
        self._controller.set_value(self._default_value)

    def _reset_values_to_cycle(self) -> None:
        """Reload values from config and validate them."""
        self._values_to_cycle = self._config.read()

        if len(set(self._values_to_cycle)) != len(self._values_to_cycle):
            raise ValueError("Values to cycle does not support duplicates.")

        # Duplicate first value at the end, to allow cycling
        if self._values_to_cycle:
            self._values_to_cycle.append(self._values_to_cycle[0])

    def _read_default_value(self, value: T | None) -> T:
        """Read value from controller if it was not given."""
        if (default := self._controller.DEFAULT_VALUE) is None:
            raise ValueError(
                f"{self._controller} can't be used with MultipleAssignment.")
        return value if value is not None else default
