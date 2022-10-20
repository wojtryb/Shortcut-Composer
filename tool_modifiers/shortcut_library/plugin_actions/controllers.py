from typing import Any

from ..convenience_utils.krita_api_wrapper import Krita
from ..convenience_utils.enums import Tool


class Controller:

    default_value: Any = None

    def get_value(self):
        pass

    def set_value(self, value):
        pass


class ToolController(Controller):

    default_value: Tool = Tool.freehand_brush

    @staticmethod
    def get_value() -> Tool:
        """Get currently active tool."""
        return Tool(Krita.get_current_tool_name())

    @staticmethod
    def set_value(value: Tool):
        """Set a passed tool."""
        Krita.trigger_action(value.value)


class PresetController(Controller):

    presets = Krita.get_presets()

    @staticmethod
    def get_value() -> str:
        """Get currently active preset."""
        return Krita.get_active_view().current_brush_preset_name()

    def set_value(self, value: str):
        """Set a preset of passed name."""
        Krita.get_active_view().set_brush_preset(self.presets[value])


class BlendingModeController(Controller):

    default_value = "normal"

    @staticmethod
    def get_value() -> str:
        """Get currently active blending mode."""
        return Krita.get_active_view().current_blending_mode()

    @staticmethod
    def set_value(value: str):
        """Set a passed blending mode."""
        Krita.get_active_view().set_blending_mode(value)


class OpacityController(Controller):

    default_value: int = 1.0

    @staticmethod
    def get_value() -> float:
        """Get current brush opacity."""
        return Krita.get_active_view().current_opacity()

    @staticmethod
    def set_value(value: float):
        """Set passed brush opacity."""
        Krita.get_active_view().set_opacity(value)
