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
        Krita.trigger_action(value)

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


@dataclass
class CyclicBlendingModes(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str

    def _set_value(self, value: str):
        print("setting", value)
        Krita.get_active_view().set_blending_mode(value)

    def _get_current_value(self) -> str:
        print(Krita.get_active_view().current_blending_mode())
        return Krita.get_active_view().current_blending_mode()


class CyclicOpacity(CyclicPluginAction):

    def __init__(
        self,
        action_name: str,
        _values_to_cycle: List[float],
        _default_value: float
    ):
        self.action_name = action_name
        self._values_to_cycle = [round(val/100, 4) for val in _values_to_cycle]
        self._default_value = round(_default_value/100, 4)

    def _set_value(self, value: float):
        Krita.get_active_view().set_opacity(value)

    def _get_current_value(self) -> float:
        return Krita.get_active_view().current_opacity()
