from dataclasses import dataclass
from typing import List

from .krita_api_wrapper import Krita
from .interfaces import CyclicPluginAction
from .enums import Tool, BlendingMode


@dataclass
class CyclicTool(CyclicPluginAction):
    """
    Cycles around tools passed in list. Long press goes back to default_tool.

    action_name: name of action in settings
    values_to_cycle: list of tools to cycle around
    default_value (optional): tool to go back to
    include_default_in_cycle (optional): should the default tool be included
        in cycling
    time_interval (optional): time after which key press is considered long
    """

    values_to_cycle: List[Tool]
    default_value: str = Tool.freehand_brush
    include_default_in_cycle: bool = False
    time_interval: float = 0.3

    def _set_value(self, value: Tool) -> None:
        """Set a passed tool."""
        Krita.trigger_action(value.value)

    def _get_current_value(self) -> Tool:
        """Get currently active tool."""
        return Tool(Krita.get_current_tool_name())


@dataclass
class CyclicPreset(CyclicPluginAction):
    """
    Cycles around presets passed in list. Long press goes back to default one.

    action_name: name of action in settings
    values_to_cycle: list of presets to cycle around
    default_value: preset to go back to
    include_default_in_cycle (optional): should the default preset be included
        in cycling
    time_interval (optional): time after which key press is considered long
    """

    include_default_in_cycle: bool = False
    time_interval: float = 0.3

    def _set_value(self, value: str):
        """Set a preset of passed name."""
        presets = Krita.get_presets()
        Krita.get_active_view().set_brush_preset(presets[value])

    def _get_current_value(self) -> str:
        """Get currently active preset."""
        return Krita.get_active_view().current_brush_preset_name()


@dataclass
class CyclicBlendingModes(CyclicPluginAction):
    """
    Cycles around blending modes. Long press goes back to default mode.

    action_name: name of action in settings
    values_to_cycle: list of blending modes to cycle around
    default_value (optional): blending mode to go back to
    include_default_in_cycle (optional): should the default mode be included
        in cycling
    time_interval (optional): time after which key press is considered long
    """

    values_to_cycle: List[BlendingMode]
    default_value: str = BlendingMode.normal
    include_default_in_cycle: bool = True
    time_interval: float = 0.3

    def _set_value(self, value: BlendingMode):
        """Set a passed blending mode."""
        Krita.get_active_view().set_blending_mode(value.value)

    def _get_current_value(self) -> str:
        """Get currently active blending mode."""
        return Tool(Krita.get_active_view().current_blending_mode())


@dataclass
class CyclicOpacity(CyclicPluginAction):
    """
    Cycles around opacities. Long press goes back to default opacity.

    Opacity should be given in range <0-100>

    action_name: name of action in settings
    values_to_cycle: list of opacities to cycle around
    default_value (optional): opacities to go back to
    include_default_in_cycle (optional): should the default one be included
        in cycling
    time_interval (optional): time after which key press is considered long
    """

    default_value: float = 100.0
    include_default_in_cycle: bool = True
    time_interval: float = 0.3

    def __post_init__(self):
        super().__post_init__()
        self.values_to_cycle = \
            [round(val/100, 4) for val in self.values_to_cycle]
        self.default_value = round(self.default_value/100, 4)

    def _set_value(self, value: float):
        """Set passed brush opacity."""
        Krita.get_active_view().set_opacity(value)

    def _get_current_value(self) -> float:
        """Get current brush opacity."""
        return Krita.get_active_view().current_opacity()
