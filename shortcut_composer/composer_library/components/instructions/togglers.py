from ...api import Krita
from ..instruction_base import Instruction


class UnlockAlpha(Instruction):
    def enter(self) -> 'UnlockAlpha':
        Krita.set_action_state("preserve_alpha", False)
        return self


class TurnOffEraser(Instruction):
    def enter(self) -> 'TurnOffEraser':
        Krita.set_action_state("erase_action", False)
        return self
