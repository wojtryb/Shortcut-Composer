from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from .krita_api import Krita, Node
from .enums import Tool, BlendingMode


class Controller(ABC):

    default_value: Any = None
    @abstractmethod
    def get_value(self): ...
    @abstractmethod
    def set_value(self, value): ...


class SetBrushStrategy(Enum):
    @staticmethod
    def __always(): ToolController.set_value(Tool.FREEHAND_BRUSH)

    @staticmethod
    def __never(): ...

    @staticmethod
    def __on_non_paintable():
        current_tool = ToolController.get_value()
        if not Tool.is_paintable(current_tool):
            ToolController.set_value(Tool.FREEHAND_BRUSH)

    ALWAYS = __always
    NEVER = __never
    ON_NON_PAINTABLE = __on_non_paintable


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


class PresetController(Controller):

    presets = Krita.get_presets()

    def __init__(
        self,
        set_brush_strategy=SetBrushStrategy.ON_NON_PAINTABLE
    ):
        self.set_brush_strategy = set_brush_strategy

    @staticmethod
    def get_value() -> str:
        """Get currently active preset."""
        return Krita.get_active_view().current_brush_preset_name()

    def set_value(self, value: str):
        """Set a preset of passed name."""
        self.set_brush_strategy()
        Krita.get_active_view().set_brush_preset(self.presets[value])


class BlendingModeController(Controller):

    default_value = BlendingMode.NORMAL

    @staticmethod
    def get_value() -> BlendingMode:
        """Get currently active blending mode."""
        return BlendingMode(Krita.get_active_view().current_blending_mode())

    @staticmethod
    def set_value(value: BlendingMode):
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


class FlowController(Controller):
    pass


class BrushSizeController(Controller):
    pass


class CanvasZoomController(Controller):
    def get_value(self) -> float:
        return Krita.get_active_canvas().zoom()

    def set_value(self, value: float):
        Krita.get_active_canvas().set_zoom(value)


class CanvasRotationController(Controller):
    def get_value(self) -> float:
        return Krita.get_active_canvas().rotation()

    def set_value(self, value: float):
        Krita.get_active_canvas().set_rotation(value)
