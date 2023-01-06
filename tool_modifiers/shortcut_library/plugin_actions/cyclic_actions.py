from dataclasses import dataclass
from typing import List
from krita import Krita

from ._interfaces import CyclicPluginAction
from ._helpers import get_current_tool_name


@dataclass
class CyclicTool(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str = "KritaShape/KisToolBrush"

    def _set_value(self, value: str) -> None:
        'activates a tool of passed name'
        Krita.instance().action(value).trigger()

    def _get_current_value(self) -> str:
        return get_current_tool_name()


@dataclass
class CyclicPreset(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str

    def _set_value(self, value: str):
        presets = Krita.instance().resources('preset')

        current_view = Krita.instance().activeWindow().activeView()
        current_view.setCurrentBrushPreset(presets[value])

    def _get_current_value(self) -> str:
        current_view = Krita.instance().activeWindow().activeView()
        return current_view.currentBrushPreset().name()


class CyclicBlendingModes(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str

    def _set_value(self, value: str):
        current_view = Krita.instance().activeWindow().activeView()
        current_view.setCurrentBlendingMode(value)

    def _get_current_value(self) -> str:
        current_view = Krita.instance().activeWindow().activeView()
        return current_view.currentBlendingMode()


class CyclicOpacity(CyclicPluginAction):

    action_name: int
    _values_to_cycle: List[int]
    _default_value: int

    def _set_value(self, value: int):
        current_view = Krita.instance().activeWindow().activeView()
        current_view.setPaintingOpacity(value)

    def _get_current_value(self) -> int:
        current_view = Krita.instance().activeWindow().activeView()
        return current_view.paintingOpacity()
