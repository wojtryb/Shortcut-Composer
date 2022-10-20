from krita import Krita
from dataclasses import dataclass

from ._interfaces import TemporaryAction
from ._helpers import get_current_tool_name
from ...config import connected_toggles


@dataclass
class TemporaryTool(TemporaryAction):

    action_name: str
    _krita_tool_name: str
    _default_tool_name: str = "KritaShape/KisToolBrush"

    def _set_low(self):
        Krita.instance().action(self._default_tool_name).trigger()

    def _set_high(self):
        Krita.instance().action(self._krita_tool_name).trigger()

    def _is_high_state(self):
        'returns True if the passed tool is active'
        return get_current_tool_name() == self._krita_tool_name


class TemporaryEraser(TemporaryAction):

    def __init__(self):
        self.action_name = 'Eraser (toggle)'

    def _set_low(self):
        self._toggle_eraser()

    def _set_high(self):
        self._toggle_eraser()

    def _is_high_state(self):
        'returns True if the passed tool is active'
        Krita.instance().action("erase_action").isChecked()

    @staticmethod
    def _toggle_eraser():
        'changes the state of the eraser, may affect alpha lock'
        if connected_toggles:
            Krita.instance().action("preserve_alpha").setChecked(False)
        Krita.instance().action("erase_action").trigger()


class TemporaryAlphaLock(TemporaryAction):

    def __init__(self):
        self.action_name = 'Preserve alpha (toggle)'

    def _set_low(self):
        self._toggle_alpha_lock()

    def _set_high(self):
        self._toggle_alpha_lock()

    def _is_high_state(self):
        'returns True if the alpha is locked'
        return Krita.instance().action("preserve_alpha").isChecked()

    @staticmethod
    def _toggle_alpha_lock():
        'changes the state of the alpha lock, may affect the eraser'
        if connected_toggles:
            Krita.instance().action("erase_action").setChecked(False)
        Krita.instance().action("preserve_alpha").trigger()
