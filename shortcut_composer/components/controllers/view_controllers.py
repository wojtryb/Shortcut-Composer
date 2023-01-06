from api_krita import Krita
from api_krita.enums import BlendingMode
from ..controller_base import Controller


class PresetController(Controller):
    """
    Gives access to presets.

    - Operates on strings with preset names
    - Does not have a default
    """

    presets = Krita.get_presets()

    @staticmethod
    def get_value() -> str:
        """Get currently active preset."""
        return Krita.get_active_view().current_brush_preset_name()

    def set_value(self, value: str) -> None:
        """Set a preset of passed name."""
        Krita.get_active_view().set_brush_preset(self.presets[value])


class BrushSizeController(Controller):
    """
    Gives access to brush size.

    - Operates on integers representing brush size in pixels
    - Defaults to `100`
    """

    default_value: int = 100

    @staticmethod
    def get_value() -> float:
        return Krita.get_active_view().current_brush_size()

    @staticmethod
    def set_value(value: float) -> None:
        Krita.get_active_view().set_brush_size(value)


class BlendingModeController(Controller):
    """
    Gives access to brush blending mode.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

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
    """
    Gives access to brush opacity in %.

    - Operates on integers `<0-100>`
    - Defaults to `100`
    """

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
    """
    Gives access to brush flow in %.

    - Operates on integers `<0-100>`
    - Defaults to `100`
    """

    default_value: int = 100

    @staticmethod
    def get_value() -> int:
        return Krita.get_active_view().current_flow()

    @staticmethod
    def set_value(value: int) -> None:
        Krita.get_active_view().set_flow(value)
