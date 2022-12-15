from typing import List, Optional

from composer_utils import Config
from core_components import InstructionHolder, Instruction


class PluginAction:
    """
    Stores basic action attributes and grants main plugin action interface.

    ### Arguments:

    - `name`         -- unique name of action. Must match the definition
                        in shortcut_composer.action file
    - `instructions` -- (optional) list of additional instructions to
                        perform on key press and release.
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long.

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
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        self.name = name
        if short_vs_long_press_time is None:
            short_vs_long_press_time = Config.SHORT_VS_LONG_PRESS_TIME.get()
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
