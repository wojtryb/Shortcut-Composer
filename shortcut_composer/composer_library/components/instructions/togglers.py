from dataclasses import dataclass

from ...api import Krita
from ..instruction_base import Instruction
from ...api.enums import Toggle


@dataclass
class TemporaryToggle(Instruction):

    toggle: Toggle

    def enter(self) -> 'TurnOff':
        Krita.trigger_action(self.toggle)
        return self

    def exit(self, *_) -> None:
        Krita.trigger_action(self.toggle)


@dataclass
class TurnOn(Instruction):

    toggle: Toggle

    def enter(self) -> 'TurnOn':
        Krita.set_toggle_state(self.toggle, True)
        return self


@dataclass
class TurnOff(Instruction):

    toggle: Toggle

    def enter(self) -> 'TurnOff':
        Krita.set_toggle_state(self.toggle, False)
        return self


@dataclass
class TemporaryOn(Instruction):

    toggle: Toggle

    def enter(self) -> 'TurnOff':
        Krita.set_toggle_state(self.toggle, True)
        return self

    def exit(self, *_) -> None:
        Krita.set_toggle_state(self.toggle, False)


@dataclass
class TemporaryOff(Instruction):

    toggle: Toggle

    def enter(self) -> 'TurnOff':
        Krita.set_toggle_state(self.toggle, False)
        return self

    def exit(self, *_) -> None:
        Krita.set_toggle_state(self.toggle, True)
