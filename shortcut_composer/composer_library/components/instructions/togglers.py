from dataclasses import dataclass
from functools import partialmethod

from ...api import Krita
from ..instruction_base import Instruction
from ...api.enums import Toggle


def _set_toggle(self, state: bool, *_) -> Instruction:
    Krita.set_toggle_state(self.toggle, state)
    return self


@dataclass
class _ToggleInstruction(Instruction):

    toggle: Toggle


class TurnOn(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=True)


class TurnOff(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=False)


class TemporaryOn(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=True)
    exit = partialmethod(_set_toggle, state=False)


class TemporaryOff(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=False)
    exit = partialmethod(_set_toggle, state=True)
