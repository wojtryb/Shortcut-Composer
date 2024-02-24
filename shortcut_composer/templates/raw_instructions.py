# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from composer_utils import Config
from core_components import InstructionHolder, Instruction
from input_adapter import ComplexActionInterface


class RawInstructions(ComplexActionInterface):
    """
    ShortcutComposer action base.

    Handles passed instructions, implementing ComplexActionInterface.

    ### Arguments:

    - `name`         -- unique name of action. Must match the definition
                        in shortcut_composer.action file
    - `instructions` -- (optional) list of additional instructions to
                        perform on key press and release.
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long.

    ### Action implementation example:

    Example action is meant to turn on ISOLATE_LAYER action for as long
    as the key is pressed.

    ```python
    templates.RawInstructions(
        name="Toggle isolate layer (temporary)",
        instructions=[
            instructions.TemporaryOn(Toggle.ISOLATE_LAYER)
        ],
        short_vs_long_press_time=0.3
    )
    ```
    """

    def __init__(
        self,
        name: str,
        instructions: list[Instruction] | None = None,
        short_vs_long_press_time: float | None = None
    ) -> None:
        self.name = name
        self.short_vs_long_press_time = _read_time(short_vs_long_press_time)
        self._instructions = InstructionHolder(
            instructions if instructions is not None else [])

    def on_key_press(self) -> None:
        """Run instructions meant for key press event."""
        self._instructions.on_key_press()

    def on_short_key_release(self) -> None:
        """Run instructions meant for key release event."""
        self._instructions.on_short_key_release()

    def on_long_key_release(self) -> None:
        """Run instructions meant for key release event after long time."""
        self._instructions.on_long_key_release()

    def on_every_key_release(self) -> None:
        """Run instructions meant for key release event after short time."""
        self._instructions.on_every_key_release()


def _read_time(short_vs_long_press_time: float | None) -> float:
    """Return the given time, or time red from krita config if not given."""
    if short_vs_long_press_time is None:
        return Config.SHORT_VS_LONG_PRESS_TIME.read()
    return short_vs_long_press_time
