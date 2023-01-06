from dataclasses import dataclass
from functools import partialmethod

from api_krita import Krita
from api_krita.enums import Toggle
from ..instruction_base import Instruction


def _set_toggle(self, state: bool, *_) -> None:
    Krita.set_toggle_state(self.toggle, state)


@dataclass
class _ToggleInstruction(Instruction):

    toggle: Toggle


class EnsureOn(_ToggleInstruction):

    on_key_press = partialmethod(_set_toggle, state=True)


class EnsureOff(_ToggleInstruction):

    on_key_press = partialmethod(_set_toggle, state=False)


class TemporaryOn(_ToggleInstruction):

    on_key_press = partialmethod(_set_toggle, state=True)
    on_every_key_release = partialmethod(_set_toggle, state=False)


class TemporaryOff(_ToggleInstruction):

    on_key_press = partialmethod(_set_toggle, state=False)
    on_every_key_release = partialmethod(_set_toggle, state=True)
