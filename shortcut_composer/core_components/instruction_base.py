# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import partialmethod


class Instruction:
    """
    Component that allows to perform additional tasks outside the main logic.

    Depending on the picked instruction, tasks can be performed on key
    press and release.
    """

    def on_key_press(self) -> None: ...
    def on_short_key_release(self) -> None: ...
    def on_long_key_release(self) -> None: ...
    def on_every_key_release(self) -> None: ...


class InstructionHolder:
    """
    Instruction container.

    Has the same interface as Instruction. Each method runs the
    respective method in every stored Instruction.
    """

    def __init__(self, instructions: list[Instruction]) -> None:
        self._instructions = instructions

    def append(self, instruction: Instruction) -> None:
        """Add new instruction to the list on runtime."""
        self._instructions.append(instruction)

    def _template(self, method_name: str) -> None:
        """Perform method `method_name` of each held instruction."""
        for instruction in self._instructions:
            getattr(instruction, method_name)()

    on_key_press = partialmethod(_template, "on_key_press")
    on_short_key_release = partialmethod(_template, "on_short_key_release")
    on_long_key_release = partialmethod(_template, "on_long_key_release")
    on_every_key_release = partialmethod(_template, "on_every_key_release")
