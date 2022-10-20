from dataclasses import dataclass
from krita import Krita

from ._interfaces import PluginAction
from ._helpers import get_current_tool_name
from ...config import connected_toggles


@dataclass
class TemporaryTool(PluginAction):

    action_name: str
    krita_tool: str
    default_tool: str = "KritaShape/KisToolBrush"

    def set_low(self):
        self._set_tool(self.default_tool)

    def set_high(self):
        self._set_tool(self.krita_tool)

    def is_high_state(self):
        'returns True if the passed tool is active'
        return get_current_tool_name() == self.krita_tool

    @staticmethod
    def _set_tool(tool_name):
        'activates a tool of passed name'
        Krita.instance().action(tool_name).trigger()


class TemporaryEraser(PluginAction):

    def __init__(self):
        self.action_name = 'Eraser (toggle)'

    def set_low(self):
        self._toggle_eraser()

    def set_high(self):
        self._toggle_eraser()

    def is_high_state(self):
        'returns True if the passed tool is active'
        krita_eraser_action = Krita.instance().action("erase_action")
        return krita_eraser_action.isChecked()

    @staticmethod
    def _toggle_eraser():
        'changes the state of the eraser, may affect alpha lock'
        if connected_toggles:
            Krita.instance().action("preserve_alpha").setChecked(False)
        Krita.instance().action("erase_action").trigger()


class TemporaryAlphaLock(PluginAction):

    def __init__(self):
        self.action_name = 'Preserve alpha (toggle)'

    def set_low(self):
        self._toggle_alpha_lock()

    def set_high(self):
        self._toggle_alpha_lock()

    def is_high_state(self):
        'returns True if the alpha is locked'
        krita_preserve_alpha_action = Krita.instance().action("preserve_alpha")
        return krita_preserve_alpha_action.isChecked()

    @staticmethod
    def _toggle_alpha_lock():
        'changes the state of the alpha lock, may affect the eraser'
        if connected_toggles:
            Krita.instance().action("erase_action").setChecked(False)
        Krita.instance().action("preserve_alpha").trigger()
