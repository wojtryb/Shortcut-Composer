from dataclasses import dataclass
from typing import List

from .krita_api_wrapper import Krita
from ._interfaces import CyclicPluginAction


@dataclass
class CyclicTool(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str = "KritaShape/KisToolBrush"

    def _set_value(self, value: str) -> None:
        'activates a tool of passed name'
        Krita.instance().action(value).trigger()

    def _get_current_value(self) -> str:
        return Krita.get_current_tool_name()


@dataclass
class CyclicPreset(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str

    def _set_value(self, value: str):
        presets = Krita.get_presets()
        Krita.get_active_view().set_brush_preset(presets[value])

    def _get_current_value(self) -> str:
        return Krita.get_active_view().current_brush_preset_name()


class CyclicBlendingModes(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str

    def _set_value(self, value: str):
        Krita.get_active_view().set_blending_mode(value)

    def _get_current_value(self) -> str:
        return Krita.get_active_view().current_blending_mode()


class CyclicOpacity(CyclicPluginAction):

    action_name: int
    _values_to_cycle: List[int]
    _default_value: int

    def _set_value(self, value: int):
        Krita.get_active_view().set_opacity(value)

    def _get_current_value(self) -> int:
        return Krita.get_active_view().current_opacity()
