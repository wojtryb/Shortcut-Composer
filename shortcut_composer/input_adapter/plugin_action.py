from typing import List

from shortcut_composer_config import SHORT_VS_LONG_PRESS_TIME
from core_components import Controller, InstructionHolder, Instruction


class PluginAction:
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
    """
    Class is meant for creating child classes which override:
    - on_key_press
    - on_short_key_release
    - on_long_key_release
    - on_every_key_release
    """

    def __init__(
        self, *,
        name: str,
        instructions: List[Instruction] = [],
        short_vs_long_press_time: float = SHORT_VS_LONG_PRESS_TIME,
    ) -> None:
        self.name = name
        self.short_vs_long_press_time = short_vs_long_press_time
        self._instructions = InstructionHolder(instructions)

    def on_key_press(self) -> None:
        """Called on each press of key specified in settings."""
        self._instructions.on_key_press()

    def on_short_key_release(self) -> None:
        """Called when related key was released shortly after press."""
        self._instructions.on_short_key_release()

    def on_long_key_release(self) -> None:
        """Called when related key was released after a long time."""
        self._instructions.on_long_key_release()

    def on_every_key_release(self) -> None:
        """Called on each release of related key, after short/long callback."""
        self._instructions.on_every_key_release()
