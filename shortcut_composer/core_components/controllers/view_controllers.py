from api_krita import Krita
from api_krita.enums import BlendingMode
from ..controller_base import Controller


class ViewBasedController(Controller):

    def refresh(self):
        self.view = Krita.get_active_view()


class PresetController(ViewBasedController):
    """
    Gives access to presets.

    - Operates on strings with preset names
    - Does not have a default
    """

    def get_value(self) -> str:
        """Get currently active preset."""
        return self.view.brush_preset

    def set_value(self, value: str) -> None:
        """Set a preset of passed name."""
        self.view.brush_preset = value


class BrushSizeController(ViewBasedController):
    """
    Gives access to brush size.

    - Operates on integers representing brush size in pixels
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        return self.view.brush_size

    def set_value(self, value: int) -> None:
        self.view.brush_size = value


class BlendingModeController(ViewBasedController):
    """
    Gives access to brush blending mode.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get currently active blending mode."""
        return self.view.blending_mode

    def set_value(self, value: BlendingMode) -> None:
        """Set a passed blending mode."""
        self.view.blending_mode = value


class OpacityController(ViewBasedController):
    """
    Gives access to brush opacity in %.

    - Operates on integers `<0-100>`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get current brush opacity."""
        return self.view.opacity

    def set_value(self, value: int) -> None:
        """Set passed brush opacity."""
        self.view.opacity = value


class FlowController(ViewBasedController):
    """
    Gives access to brush flow in %.

    - Operates on integers `<0-100>`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        return self.view.current_flow

    def set_value(self, value: int) -> None:
        self.view.set_flow = value