from dataclasses import dataclass

from ...api import Krita
from ...api.wrappers import Node
from ...api.enums import Tool
from ..controller_base import Controller


class ToolController(Controller):

    default_value: Tool = Tool.FREEHAND_BRUSH

    @staticmethod
    def get_value() -> Tool:
        """Get currently active tool."""
        return Krita.get_current_tool()

    @staticmethod
    def set_value(value: Tool) -> None:
        """Set a passed tool."""
        Krita.trigger_action(value.value)


@dataclass
class EraserController(Controller):
    default_value = False

    @staticmethod
    def get_value() -> Node:
        return Krita.get_action_state("erase_action")

    def set_value(self, value: bool) -> None:
        Krita.set_action_state("erase_action", value)


@dataclass
class PreserveAlphaController(Controller):
    default_value = False

    @staticmethod
    def get_value() -> Node:
        return Krita.get_action_state("preserve_alpha")

    def set_value(self, value: bool) -> None:
        Krita.set_action_state("preserve_alpha", value)
