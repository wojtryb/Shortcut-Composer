from api_krita import Krita
from api_krita.enums import BlendingMode
from ..controller_base import Controller


class NodeBasedController(Controller):
    """Family of controllers which operate on values from active node."""

    def refresh(self):
        """Refresh currently stored active node."""
        self.active_node = Krita.get_active_document().active_node


class LayerOpacityController(NodeBasedController):
    """
    Gives access to active layers' `blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get currently active blending mode."""
        return self.active_node.opacity

    def set_value(self, opacity: int) -> None:
        """Set a passed blending mode."""
        self.active_node.opacity = opacity


class LayerBlendingModeController(NodeBasedController):
    """
    Gives access to active layers' `opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get current brush opacity."""
        return self.active_node.blending_mode

    def set_value(self, blending_mode: BlendingMode) -> None:
        """Set passed brush opacity."""
        self.active_node.blending_mode = blending_mode


class LayerVisibilityController(NodeBasedController):
    """
    Gives access to active layers' `visibility`.

    - Operates on `bool`
    - Defaults to True
    """

    default_value: bool = True

    def get_value(self) -> bool:
        """Get current brush opacity."""
        return self.active_node.visible

    def set_value(self, visibility: bool) -> None:
        """Set passed brush opacity."""
        self.active_node.visible = visibility