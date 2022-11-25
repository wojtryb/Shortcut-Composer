from typing import List, Iterator, TypeVar, Generic, Optional
from itertools import cycle

from core_components import Controller, Instruction
from input_adapter import PluginAction

T = TypeVar('T')


class MultipleAssignment(PluginAction, Generic[T]):
    """
    Cycle multiple values (short press) or return to default (long press).

    Action cycles the values in `values_to_cycle` list:
    - short key press moves to next value in list.
    - if current value does not belong to the list, start from beginning
    - when the list is exhausted, start again
    - end of long press ensures `default value`

    ### Arguments:

    - `name`            -- unique name of action. Must match the definition in
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
        name="Brush size (cycle)",
        controller=controllers.BrushSizeController(),
        default_value=100,
        values_to_cycle=[5, 10, 20, 50],
    )
    ```
    """

    def __init__(self, *,
                 name: str,
                 controller: Controller,
                 values_to_cycle: List[T],
                 default_value: Optional[T] = None,
                 instructions: List[Instruction] = [],
                 time_interval: float = 0.3) -> None:
        super().__init__(
            name=name,
            time_interval=time_interval,
            controller=controller,
            instructions=instructions)

        self.values_to_cycle = values_to_cycle
        self.default_value = self._read_default_value(default_value)

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
        self._set_value(self.default_value)
        self._reset_iterator()

    def _set_value(self, value: T) -> None:
        """Set the value using the controller, and remember it."""
        self._last_value = value
        self._controller.set_value(value)

    def _reset_iterator(self) -> None:
        """Replace the iterator with new cyclic iterator over cycled values."""
        self._iterator = cycle(self.values_to_cycle)

    def _read_default_value(self, value: Optional[T]) -> T:
        """Read value from controller if it was not given."""
        return value if value else self._controller.default_value
