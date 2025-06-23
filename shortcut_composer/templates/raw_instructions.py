# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
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

    ### Action implementation example:

    Example action is meant to turn on ISOLATE_LAYER action for as long
    as the key is pressed.

    ```python
    templates.RawInstructions(
        name="Toggle isolate layer (temporary)",
        instructions=[
            instructions.TemporaryOn(Toggle.ISOLATE_LAYER)
        ]
    )
    ```
    """

    def __init__(
        self,
        name: str,
        instructions: list[Instruction] | None = None,
    ) -> None:
        self.name = name
        self.short_vs_long_press_time = Config.SHORT_VS_LONG_PRESS_TIME.read()
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
