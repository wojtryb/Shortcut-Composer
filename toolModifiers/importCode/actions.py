from dataclasses import dataclass
from itertools import zip_longest
from typing import List
from krita import Krita
from abc import ABC, abstractmethod

from .current_tool import get_current_tool_name
from ..config import connected_toggles


class Action(ABC):
    action_name: str

    def set_low(self):
        pass

    def set_high(self):
        pass

    def is_high_state(self):
        pass


@dataclass
class ToolWrapper(Action):
    action_name: str
    default_tool: str = "KritaShape/KisToolBrush"

    def set_low(self):
        self._set_tool(self.default_tool)

    def set_high(self):
        self._set_tool(self.krita_name)

    def is_high_state(self):
        'returns True if the passed tool is active'
        return get_current_tool_name() == self.krita_name

    @staticmethod
    def _set_tool(tool_name):
        'activates a tool of passed name'
        Krita.instance().action(tool_name).trigger()


class CyclicShortcut(Action):
    action_name: str
    values: List[str]
    default_value: str

    @abstractmethod
    def _set_value(self, value: str) -> None:
        pass

    @abstractmethod
    def _get_current_value(self) -> str:
        pass

    def set_low(self):
        self._set_value(self.default_value)

    def set_high(self):
        current_value = self._get_current_value()
        if current_value not in self.values:
            self._set_value(self.values[0])
            return

        for tool, next_tool in zip_longest(
                self.values,
                self.values[1:],
                fillvalue=self.values[0]):
            if tool == current_value:
                self._set_value(next_tool)
                return

    def is_high_state(self):
        return False


@dataclass
class CyclicTool(CyclicShortcut):
    action_name: str
    values: List[str]
    default_value: str = "KritaShape/KisToolBrush"

    def _set_value(self, value: str) -> None:
        'activates a tool of passed name'
        Krita.instance().action(value).trigger()

    def _get_current_value(self) -> str:
        return get_current_tool_name()


class EraserWrapper(Action):
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


class AlphaWrapper(Action):
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
