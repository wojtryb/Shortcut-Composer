from dataclasses import dataclass
from typing import List

from .krita_api_wrapper import Krita
from ._interfaces import CyclicPluginAction
from .enums import Tool, BlendingMode


@dataclass
class CyclicTool(CyclicPluginAction):

    values_to_cycle: List[Tool]
    default_value: str = Tool.freehand_brush
    time_interval: float = 0.3
    include_default_in_cycle: bool = False

    def _set_value(self, value: Tool) -> None:
        'activates a tool of passed name'
        Krita.trigger_action(value.value)

    def _get_current_value(self) -> str:
        return Tool(Krita.get_current_tool_name())


@dataclass
class CyclicPreset(CyclicPluginAction):

    time_interval: float = 0.3
    include_default_in_cycle: bool = False

    def _set_value(self, value: str):
        presets = Krita.get_presets()
        Krita.get_active_view().set_brush_preset(presets[value])

    def _get_current_value(self) -> str:
        return Krita.get_active_view().current_brush_preset_name()


@dataclass
class CyclicBlendingModes(CyclicPluginAction):

    values_to_cycle: List[BlendingMode]
    default_value: str = BlendingMode.normal
    time_interval: float = 0.3
    include_default_in_cycle: bool = True

    def _set_value(self, value: BlendingMode):
        Krita.get_active_view().set_blending_mode(value.value)

    def _get_current_value(self) -> str:
        return Tool(Krita.get_active_view().current_blending_mode())


@dataclass
class CyclicOpacity(CyclicPluginAction):

    default_value: float = 100.0
    time_interval: float = 0.3
    include_default_in_cycle: bool = True

    def __post_init__(self):
        super().__post_init__()
        self.values_to_cycle = \
            [round(val/100, 4) for val in self.values_to_cycle]
        self.default_value = round(self.default_value/100, 4)

    def _set_value(self, value: float):
        Krita.get_active_view().set_opacity(value)

    def _get_current_value(self) -> float:
        return Krita.get_active_view().current_opacity()
