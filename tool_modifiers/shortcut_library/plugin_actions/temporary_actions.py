from dataclasses import dataclass

from .krita_api_wrapper import Krita
from ._interfaces import TemporaryAction
from ...config import connected_toggles


@dataclass
class TemporaryTool(TemporaryAction):

    action_name: str
    _krita_tool_name: str
    _default_tool_name: str = "KritaShape/KisToolBrush"

    def _set_low(self):
        Krita.trigger_action(self._default_tool_name)

    def _set_high(self):
        Krita.trigger_action(self._krita_tool_name)

    def _is_high_state(self):
        'returns True if the passed tool is active'
        return Krita.get_current_tool_name() == self._krita_tool_name


class TemporaryEraser(TemporaryAction):

    def __init__(self):
        self.action_name = 'Eraser (toggle)'

    def _set_low(self):
        self._toggle_eraser()

    def _set_high(self):
        self._toggle_eraser()

    def _is_high_state(self):
        'returns True if the passed tool is active'
        Krita.get_action_state("erase_action")

    @staticmethod
    def _toggle_eraser():
        'changes the state of the eraser, may affect alpha lock'
        if connected_toggles:
            Krita.set_action_state("preserve_alpha", False)
        Krita.trigger_action("erase_action")


class TemporaryAlphaLock(TemporaryAction):

    def __init__(self):
        self.action_name = 'Preserve alpha (toggle)'

    def _set_low(self):
        self._toggle_alpha_lock()

    def _set_high(self):
        self._toggle_alpha_lock()

    def _is_high_state(self):
        'returns True if the alpha is locked'
        Krita.get_action_state("preserve_alpha")

    @staticmethod
    def _toggle_alpha_lock():
        'changes the state of the alpha lock, may affect the eraser'
        if connected_toggles:
            Krita.set_action_state("erase_action", False)
        Krita.trigger_action("preserve_alpha")
