from typing import List, TypeVar

from core_components import Instruction
from input_adapter import PluginAction

T = TypeVar('T')


class RawInstructions(PluginAction):
    """
    Temporarily toggle plugin instructions.

    Action starts all the instructions on key press, and ends them on
    release. Short and long presses are not distinguished.

    ### Arguments:

    - `name`          -- unique name of action. Must match the
                          definition in shortcut_composer.action file
    - `instructions`  -- list of additional instructions to perform on
                          key press and release.

    ### Action implementation example:

    Example action is meant to turn on ISOLATE_LAYER action for the time
    a key is pressed.

    ```python
    RawInstructions(
        name="Toggle isolate layer (temporary)",
        instructions=[
            instructions.TemporaryOn(Toggle.ISOLATE_LAYER)
        ]
    )
    ```
    """

    def __init__(self, *,
                 name: str,
                 instructions: List[Instruction]) -> None:
        super().__init__(
            name=name,
            instructions=instructions,
            time_interval=0.0)

    def on_key_press(self) -> None:
        """Enter all instructions on every key press."""
        self._instructions.enter()

    def on_every_key_release(self) -> None:
        """End the instructions on every key release."""
        self._instructions.exit()
