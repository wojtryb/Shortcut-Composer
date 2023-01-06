from dataclasses import dataclass

from .krita_api_wrapper import Krita
from ._interfaces import TemporaryAction


@dataclass
class TemporaryTool(TemporaryAction):

    action_name: str
    krita_tool_name: str
    default_tool_name: str = "KritaShape/KisToolBrush"
    time_interval: float = 0.3

    def _set_low(self):
        Krita.trigger_action(self.default_tool_name)

    def _set_high(self):
        Krita.trigger_action(self.krita_tool_name)

    def _is_high_state(self):
        'returns True if the passed tool is active'
        return Krita.get_current_tool_name() == self.krita_tool_name


@dataclass
class TemporaryEraser(TemporaryAction):

    time_interval: float = 0.3
    connected_toggles: bool = True

    def __init__(self):
        self.action_name = 'Eraser (toggle)'

    def _set_low(self):
        self._toggle_eraser()

    def _set_high(self):
        self._toggle_eraser()

    def _is_high_state(self):
        'returns True if the passed tool is active'
        Krita.get_action_state("erase_action")

    def _toggle_eraser(self):
        'changes the state of the eraser, may affect alpha lock'
        if self.connected_toggles:
            Krita.set_action_state("preserve_alpha", False)
        Krita.trigger_action("erase_action")


@dataclass
class TemporaryAlphaLock(TemporaryAction):

    action_name: str = 'Preserve alpha (toggle)'
    time_interval: float = 0.3
    connected_toggles: bool = True

    def _set_low(self):
        self._toggle_alpha_lock()

    def _set_high(self):
        self._toggle_alpha_lock()

    def _is_high_state(self):
        'returns True if the alpha is locked'
        Krita.get_action_state("preserve_alpha")

    def _toggle_alpha_lock(self):
        'changes the state of the alpha lock, may affect the eraser'
        if self.connected_toggles:
            Krita.set_action_state("erase_action", False)
        Krita.trigger_action("preserve_alpha")
