from ...api import Krita
from ...api.enums import BlendingMode
from ..controller_base import Controller
from .strategies.set_brush_strategy import SetBrushStrategy


class PresetController(Controller):

    presets = Krita.get_presets()

    def __init__(self, set_brush_strategy=SetBrushStrategy.ON_NON_PAINTABLE):
        self.set_brush_strategy = set_brush_strategy

    @staticmethod
    def get_value() -> str:
        """Get currently active preset."""
        return Krita.get_active_view().current_brush_preset_name()

    def set_value(self, value: str) -> None:
        """Set a preset of passed name."""
        self.set_brush_strategy()
        Krita.get_active_view().set_brush_preset(self.presets[value])


class BrushSizeController(Controller):

    default_value: int = 100

    @staticmethod
    def get_value() -> float:
        return Krita.get_active_view().current_brush_size()

    @staticmethod
    def set_value(value: float) -> None:
        Krita.get_active_view().set_brush_size(value)


class BlendingModeController(Controller):

    default_value = BlendingMode.NORMAL

    @staticmethod
    def get_value() -> BlendingMode:
        """Get currently active blending mode."""
        return BlendingMode(Krita.get_active_view().current_blending_mode())

    @staticmethod
    def set_value(value: BlendingMode) -> None:
        """Set a passed blending mode."""
        Krita.get_active_view().set_blending_mode(value)


class OpacityController(Controller):

    default_value: int = 100

    @staticmethod
    def get_value() -> int:
        """Get current brush opacity."""
        return Krita.get_active_view().current_opacity()

    @staticmethod
    def set_value(value: int) -> None:
        """Set passed brush opacity."""
        Krita.get_active_view().set_opacity(value)


class FlowController(Controller):

    default_value: int = 100

    @staticmethod
    def get_value() -> int:
        return Krita.get_active_view().current_flow()

    @staticmethod
    def set_value(value: int) -> None:
        Krita.get_active_view().set_flow(value)
