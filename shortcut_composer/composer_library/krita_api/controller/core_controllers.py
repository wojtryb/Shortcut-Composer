from ..core_api import Krita
from ..wrappers import Node
from ..enums import Tool
from .base import Controller


class ToolController(Controller):

    default_value: Tool = Tool.FREEHAND_BRUSH

    @staticmethod
    def get_value() -> Tool:
        """Get currently active tool."""
        return Krita.get_current_tool()

    @staticmethod
    def set_value(value: Tool):
        """Set a passed tool."""
        Krita.trigger_action(value.value)


class EraserController(Controller):

    default_value: bool = False

    def __init__(self, affect_preserve_alpha: bool = True):
        self.affect_preserve_alpha = affect_preserve_alpha

    @staticmethod
    def get_value() -> Node:
        return Krita.get_action_state("erase_action")

    def set_value(self, value: bool):
        if self.affect_preserve_alpha:
            Krita.set_action_state("preserve_alpha", False)
        Krita.set_action_state("erase_action", value)


class PreserveAlphaController(Controller):

    default_value: bool = False

    def __init__(self, affect_eraser: bool = True):
        self.affect_eraser = affect_eraser

    @staticmethod
    def get_value() -> Node:
        return Krita.get_action_state("preserve_alpha")

    def set_value(self, value: bool):
        if self.affect_eraser:
            Krita.set_action_state("erase_action", False)
        Krita.set_action_state("preserve_alpha", value)
