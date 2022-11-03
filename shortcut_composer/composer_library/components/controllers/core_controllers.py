from dataclasses import dataclass

from ...api import Krita
from ...api.wrappers import Node
from ...api.enums import Tool
from ..controller_base import Controller
from .strategies.set_brush_strategy import SetBrushStrategy


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

    affect_preserve_alpha: bool = True
    set_brush_strategy: SetBrushStrategy = SetBrushStrategy.ON_NON_PAINTABLE

    default_value = False

    @staticmethod
    def get_value() -> Node:
        return Krita.get_action_state("erase_action")

    def set_value(self, value: bool) -> None:
        self.set_brush_strategy()
        if self.affect_preserve_alpha:
            Krita.set_action_state("preserve_alpha", False)
        Krita.set_action_state("erase_action", value)


@dataclass
class PreserveAlphaController(Controller):

    affect_eraser: bool = True
    set_brush_strategy: SetBrushStrategy = SetBrushStrategy.ON_NON_PAINTABLE

    default_value = False

    @staticmethod
    def get_value() -> Node:
        return Krita.get_action_state("preserve_alpha")

    def set_value(self, value: bool) -> None:
        self.set_brush_strategy()
        if self.affect_eraser:
            Krita.set_action_state("erase_action", False)
        Krita.set_action_state("preserve_alpha", value)
