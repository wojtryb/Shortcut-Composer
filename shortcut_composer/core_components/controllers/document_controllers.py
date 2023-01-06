from api_krita import Krita
from api_krita.wrappers import Node
from ..controller_base import Controller


class LayerController(Controller):
    """
    Gives access to nodes (layers, masks etc.) from layer stack.

    - Operates on internal Layer objects. Use `CurrentLayerStack()` to
      always use current layer stack
    - Does not have a default
    """

    @staticmethod
    def get_value() -> Node:
        """Get current node."""
        return Krita.get_active_document().current_node()

    @staticmethod
    def set_value(value: Node) -> None:
        """Set passed node as current."""
        Krita.get_active_document().set_current_node(value)


class TimeController(Controller):
    """
    Gives access to animation timeline.

    - Operates on positive integers representing frame numbers
    - Defaults to 0
    """

    default_value = 0

    @staticmethod
    def get_value() -> int:
        return Krita.get_active_document().current_time()

    @staticmethod
    def set_value(value: int) -> None:
        document = Krita.get_active_document()
        if document.current_node().is_animated():
            document.set_current_time(value)
