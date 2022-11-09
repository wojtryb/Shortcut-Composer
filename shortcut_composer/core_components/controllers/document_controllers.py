from api_krita import Krita
from api_krita.wrappers import Node
from ..controller_base import Controller


class DocumentBasedController(Controller):

    def refresh(self):
        self.document = Krita.get_active_document()


class LayerController(DocumentBasedController):
    """
    Gives access to nodes (layers, masks etc.) from layer stack.

    - Operates on internal Layer objects. Use `CurrentLayerStack()` to
      always use current layer stack
    - Does not have a default
    """

    def get_value(self) -> Node:
        """Get current node."""
        return self.document.active_node

    def set_value(self, value: Node) -> None:
        """Set passed node as current."""
        self.document.active_node = value


class TimeController(DocumentBasedController):
    """
    Gives access to animation timeline.

    - Operates on positive integers representing frame numbers
    - Defaults to 0
    """

    default_value = 0

    def get_value(self) -> int:
        return self.document.current_time

    def set_value(self, value: int) -> None:
        document = self.document
        if document.active_node.is_animated:
            document.current_time = value