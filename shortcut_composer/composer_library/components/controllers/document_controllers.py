from ...api import Krita
from ...api.wrappers import Node
from ..controller_base import Controller


class LayerController(Controller):

    @staticmethod
    def get_value() -> Node:
        """Get current node."""
        return Krita.get_active_document().current_node()

    @staticmethod
    def set_value(value: Node) -> None:
        """Set passed node as current."""
        Krita.get_active_document().set_current_node(value)


class TimeController(Controller):

    @staticmethod
    def get_value() -> Node:
        return Krita.get_active_document().current_time()

    @staticmethod
    def set_value(value: int) -> None:
        document = Krita.get_active_document()
        if document.current_node().is_animated():
            document.set_current_time(value)
