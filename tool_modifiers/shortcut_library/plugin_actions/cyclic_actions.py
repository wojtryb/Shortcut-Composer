from dataclasses import dataclass

from .krita_api_wrapper import Krita
from ._interfaces import CyclicPluginAction


@dataclass
class CyclicTool(CyclicPluginAction):

    default_value: str = "KritaShape/KisToolBrush"
    time_interval: float = 0.3

    def _set_value(self, value: str) -> None:
        'activates a tool of passed name'
        Krita.trigger_action(value)

    def _get_current_value(self) -> str:
        return Krita.get_current_tool_name()


@dataclass
class CyclicPreset(CyclicPluginAction):

    time_interval: float = 0.3

    def _set_value(self, value: str):
        presets = Krita.get_presets()
        Krita.get_active_view().set_brush_preset(presets[value])

    def _get_current_value(self) -> str:
        return Krita.get_active_view().current_brush_preset_name()


@dataclass
class CyclicBlendingModes(CyclicPluginAction):

    default_value: str = "normal"
    time_interval: float = 0.3

    def _set_value(self, value: str):
        print("setting", value)
        Krita.get_active_view().set_blending_mode(value)

    def _get_current_value(self) -> str:
        return Krita.get_active_view().current_blending_mode()


@dataclass
class CyclicOpacity(CyclicPluginAction):

    default_value: float = 100.0
    time_interval: float = 0.3

    def __post_init__(self):
        self.values_to_cycle = \
            [round(val/100, 4) for val in self.values_to_cycle]
        self.default_value = round(self.default_value/100, 4)

    def _set_value(self, value: float):
        Krita.get_active_view().set_opacity(value)

    def _get_current_value(self) -> float:
        return Krita.get_active_view().current_opacity()
