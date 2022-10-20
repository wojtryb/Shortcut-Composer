from typing import List
from krita import Krita
from abc import ABC
from dataclasses import dataclass

from .current_tool import get_current_tool_name
from ..config import connected_toggles


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
        self._set_tool("KritaShape/KisToolBrush")

    def set_high(self):
        self._set_tool(self.krita_name)

    def is_high_state(self):
        'returns True if the passed tool is active'
        return get_current_tool_name() == self.krita_name

    @staticmethod
    def _set_tool(tool_name):
        'activates a tool of passed name'
        Krita.instance().action(tool_name).trigger()


class CyclicTool(Action):
    def __init__(self, tools: List[str]):
        self.tools = tools + [tools[0]]
        self.krita_name = 'Cyclic tool'
        self.human_name = 'Cyclic tool'

    def set_low(self):
        self._set_tool(self.tools[0])

    def set_high(self):
        current_tool = get_current_tool_name()
        for tool, next_tool in zip(self.tools, self.tools[1:]):
            if tool == current_tool:
                self._set_tool(next_tool)
                return

    def is_high_state(self):
        'returns True if the passed tool is active'
        return get_current_tool_name() not in self.tools

    @staticmethod
    def _set_tool(tool_name):
        'activates a tool of passed name'
        Krita.instance().action(tool_name).trigger()


class EraserWrapper(Action):
    def __init__(self):
        self.krita_name = 'Eraser (toggle)'
        self.human_name = 'Eraser (toggle)'

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


class AlphaWrapper(Action):
    def __init__(self):
        self.krita_name = 'Preserve alpha (toggle)'
        self.human_name = 'Preserve alpha (toggle)'

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
