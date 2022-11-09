from enum import Enum
from typing import List

from api_krita.wrappers import Document, Node


class PickStrategy(Enum):

    @staticmethod
    def __pick_all(document: Document) -> List[Node]:
        return document.get_all_nodes()

    @staticmethod
    def __pick_visible(document: Document) -> List[Node]:
        nodes = document.get_all_nodes()
        return [node for node in nodes
                if node.visible or node == document.active_node]

    @staticmethod
    def __pick_current_visibility(document: Document) -> List[Node]:
        nodes = document.get_all_nodes()
        current_visibility = document.active_node.visible
        return [node for node in nodes
                if node.visible == current_visibility]

    ALL = __pick_all
    VISIBLE = __pick_visible
    CURRENT_VISIBILITY = __pick_current_visibility
