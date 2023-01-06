# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Iterator, TypeVar, Generic, Optional
from itertools import cycle

from core_components import Controller, Instruction
from input_adapter import ComplexAction

T = TypeVar('T')


class MultipleAssignment(ComplexAction, Generic[T]):
    """
    Cycle multiple values (short press) or return to default (long press).

    Action cycles the values in `values_to_cycle` list:
    - short key press moves to next value in list.
    - if current value does not belong to the list, start from beginning
    - when the list is exhausted, start again
    - end of long press ensures `default value`

    ### Arguments:

    - `name`          -- unique name of action. Must match the
                         definition in shortcut_composer.action file
    - `controller`    -- defines which krita property will be modified
    - `values`        -- list of values compatibile with controller to cycle
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
        controller: Controller,
        values: List[T],
        default_value: Optional[T] = None,
        instructions: List[Instruction] = [],
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)

        self._controller = controller
        self._values_to_cycle = values
        self._default_value = self._read_default_value(default_value)

        self._last_value: Optional[T] = None
        self._iterator: Iterator[T]

    def on_key_press(self) -> None:
        """Use key press event only for switching to first value."""
        self._controller.refresh()
        super().on_key_press()
        if self._controller.get_value() != self._last_value:
            self._reset_iterator()
        self._set_value(next(self._iterator))

    def on_long_key_release(self) -> None:
        """Long releases set default value."""
        super().on_long_key_release()
        self._set_value(self._default_value)
        self._reset_iterator()

    def _set_value(self, value: T) -> None:
        """Set the value using the controller, and remember it."""
        self._last_value = value
        self._controller.set_value(value)

    def _reset_iterator(self) -> None:
        """Replace the iterator with new cyclic iterator over cycled values."""
        self._iterator = cycle(self._values_to_cycle)

    def _read_default_value(self, value: Optional[T]) -> T:
        """Read value from controller if it was not given."""
        return value if value else self._controller.default_value
