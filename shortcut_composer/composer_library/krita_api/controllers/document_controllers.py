from ..core_api import Krita
from ..wrappers import Node
from .base import Controller


class LayerController(Controller):

    @staticmethod
    def get_value() -> Node:
        """Get current node."""
        return Krita.get_active_document().current_node()

    @staticmethod
    def set_value(value: Node) -> None:
        """Set passed node as current."""
        Krita.get_active_document().set_current_node(value)
