from dataclasses import dataclass
from functools import partialmethod

from ...api import Krita
from ...api.enums import Toggle
from ..instruction_base import Instruction


def _set_toggle(self, state: bool, *_) -> Instruction:
    Krita.set_toggle_state(self.toggle, state)
    return self


@dataclass
class _ToggleInstruction(Instruction):

    toggle: Toggle


class EnsureOn(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=True)


class EnsureOff(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=False)


class TemporaryOn(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=True)
    exit = partialmethod(_set_toggle, state=False)


class TemporaryOff(_ToggleInstruction):

    enter = partialmethod(_set_toggle, state=False)
    exit = partialmethod(_set_toggle, state=True)
