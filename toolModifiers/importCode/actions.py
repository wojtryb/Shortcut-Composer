from krita import Krita
from .current_tool import get_current_tool_name
from abc import ABC

from dataclasses import dataclass
from ..config import connected_toggles


def set_tool(tool_name):
    'activates a tool of passed name'
    Krita.instance().action(tool_name).trigger()


class Action(ABC):
    krita_name: str
    human_name: str

    def set_low(self):
        pass

    def set_high(self):
        pass

    def is_high_state(self):
        pass


@dataclass
class ToolWrapper(Action):
    krita_name: str
    human_name: str

    def set_low(self):
        set_tool("KritaShape/KisToolBrush")

    def set_high(self):
        set_tool(self.krita_name)

    def is_high_state(self):
        'returns True if the passed tool is active'
        return get_current_tool_name() == self.krita_name


def toggle_eraser():
    'changes the state of the eraser, may affect alpha lock'
    if connected_toggles:
        Krita.instance().action("preserve_alpha").setChecked(False)
    Krita.instance().action("erase_action").trigger()


class EraserWrapper(Action):
    def __init__(self):
        self.krita_name = 'Eraser (toggle)'
        self.human_name = 'Eraser (toggle)'

    def set_low(self):
        toggle_eraser()

    def set_high(self):
        toggle_eraser()

    def is_high_state(self):
        'returns True if the passed tool is active'
        krita_eraser_action = Krita.instance().action("erase_action")
        return krita_eraser_action.isChecked()


def toggle_alpha_lock():
    'changes the state of the alpha lock, may affect the eraser'
    if connected_toggles:
        Krita.instance().action("erase_action").setChecked(False)
    Krita.instance().action("preserve_alpha").trigger()


class AlphaWrapper(Action):
    def __init__(self):
        self.krita_name = 'Preserve alpha (toggle)'
        self.human_name = 'Preserve alpha (toggle)'

    def set_low(self):
        toggle_alpha_lock()

    def set_high(self):
        toggle_alpha_lock()

    def is_high_state(self):
        'returns True if the alpha is locked'
        krita_preserve_alpha_action = Krita.instance().action("preserve_alpha")
        return krita_preserve_alpha_action.isChecked()
