# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from core_components import Controller, Instruction
from data_components import Tag
from .pie_menu_utils.pie_label_creator_utils import dispatch_pie_group_manager
from .raw_instructions import RawInstructions
from .multiple_assignment_utils import MaSettingsHandler, MaConfig

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
    )
    ```
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        values: list[T] | Tag,
        default_value: T | None = None,
        instructions: list[Instruction] | None = None,
    ) -> None:
        super().__init__(name, instructions)

        self._controller = controller
        self._group_manager = dispatch_pie_group_manager(controller)

        self._config = MaConfig(
            name=f"ShortcutComposer: {name}",
            value_type=self._controller.TYPE,
            values=values,
            default_value=self._read_default_value(default_value))

        self._instructions.append(MaSettingsHandler(
            name,
            controller,
            self._config))

    def on_key_press(self) -> None:
        """Switch to the next value or start over when value is not in list."""
        super().on_key_press()

        values = self._reset_values_to_cycle()

        if not values:
            return

        self._controller.refresh()
        current = self._controller.get_value()

        if current in values:
            id = values.index(current) + 1
            self._controller.set_value(values[id])
        else:
            self._controller.set_value(values[0])

    def on_long_key_release(self) -> None:
        """Set default value."""
        super().on_long_key_release()
        self._controller.set_value(self._config.DEFAULT_VALUE.read())

    def _reset_values_to_cycle(self) -> list[T]:
        """Reload values from config and validate them."""
        if not self._config.GROUP_MODE.read():
            values = self._config.VALUES.read()
        else:
            group = self._config.GROUP_NAME.read()
            values = self._group_manager.values_from_group(group)

        if len(set(values)) != len(values):
            raise ValueError("Values to cycle does not support duplicates.")

        # Duplicate first value at the end, to allow cycling
        if values:
            values.append(values[0])

        return values

    # TODO: this could be handled by config, if no defualt value is allowed
    def _read_default_value(self, value: T | None) -> T:
        """Read value from controller if it was not given."""
        if (default := self._controller.DEFAULT_VALUE) is None:
            raise ValueError(
                f"{self._controller} can't be used with MultipleAssignment.")
        return value if value is not None else default
