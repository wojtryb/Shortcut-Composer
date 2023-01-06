from dataclasses import dataclass

from .krita_api_wrapper import Krita
from ._interfaces import TemporaryAction
from .enums import Tools


@dataclass
class TemporaryTool(TemporaryAction):

    action_name: str
    krita_tool: Tools
    default_tool: Tools = Tools.freehand_brush
    time_interval: float = 0.3

    def _set_low(self):
        Krita.trigger_action(self.default_tool.value)

    def _set_high(self):
        Krita.trigger_action(self.krita_tool.value)

    def _is_high_state(self):
        'returns True if the passed tool is active'
        return Tools(Krita.get_current_tool_name()) == self.krita_tool


@dataclass
class TemporaryEraser(TemporaryAction):

    connected_toggles: bool = True
    time_interval: float = 0.3

    def __init__(self):
        self.action_name = 'Eraser (toggle)'

    def _set_low(self):
        self._set_eraser(False)

    def _set_high(self):
        self._set_eraser(True)

    def _is_high_state(self):
        'returns True if the passed tool is active'
        Krita.get_action_state("erase_action")

    def _set_eraser(self, state: bool):
        'changes the state of the eraser, may affect alpha lock'
        if self.connected_toggles:
            Krita.set_action_state("preserve_alpha", False)
        Krita.set_action_state("erase_action", state)


@dataclass
class TemporaryAlphaLock(TemporaryAction):

    action_name: str = 'Preserve alpha (toggle)'
    time_interval: float = 0.3
    connected_toggles: bool = True

    def _set_low(self):
        self._set_alpha_lock(False)

    def _set_high(self):
        self._set_alpha_lock(True)

    def _is_high_state(self):
        'returns True if the alpha is locked'
        Krita.get_action_state("preserve_alpha")

    def _set_alpha_lock(self, state: bool):
        'changes the state of the alpha lock, may affect the eraser'
        if self.connected_toggles:
            Krita.set_action_state("erase_action", False)
        Krita.set_action_state("preserve_alpha", state)
