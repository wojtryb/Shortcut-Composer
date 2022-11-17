from dataclasses import dataclass

from api_krita import Krita
from api_krita.enums import Toggle
from ..instruction_base import Instruction


def _set_up(self) -> None:
    Krita.set_toggle_state(self.toggle, True)


def _set_down(self) -> None:
    Krita.set_toggle_state(self.toggle, False)


@dataclass
class _ToggleInstruction(Instruction):
    toggle: Toggle


class EnsureOn(_ToggleInstruction):
    on_key_press = _set_up


class EnsureOff(_ToggleInstruction):
    on_key_press = _set_down


class TemporaryOn(_ToggleInstruction):
    on_key_press = _set_up
    on_every_key_release = _set_down


class TemporaryOff(_ToggleInstruction):
    on_key_press = _set_down
    on_every_key_release = _set_up
