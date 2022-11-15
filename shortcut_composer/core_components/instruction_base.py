from typing import List
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

    def __init__(self, instructions: List[Instruction] = []) -> None:
        self.__instructions = instructions

    def _template(self, method_name: str) -> None:
        for instruction in self.__instructions:
            getattr(instruction, method_name)()

    on_key_press = partialmethod(_template, "on_key_press")
    on_short_key_release = partialmethod(_template, "on_short_key_release")
    on_long_key_release = partialmethod(_template, "on_long_key_release")
    on_every_key_release = partialmethod(_template, "on_every_key_release")
