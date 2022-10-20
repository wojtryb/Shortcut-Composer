from abc import ABC, abstractmethod
from typing import Any

from .krita_api import Krita, Node
from .enums import Tool


class Controller(ABC):

    default_value: Any = None
    @abstractmethod
    def get_value(self): ...
    @abstractmethod
    def set_value(self, value): ...


class ToolController(Controller):

    default_value: Tool = Tool.FREEHAND_BRUSH

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


class LayerController(Controller):

    @staticmethod
    def get_value() -> Node:
        """Get current node."""
        return Krita.get_active_document().current_node()

    @staticmethod
    def set_value(value: Node):
        """Set passed node as current."""
        Krita.get_active_document().set_current_node(value)
