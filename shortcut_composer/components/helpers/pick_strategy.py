from enum import Enum
from typing import List

from api_krita.wrappers import Document, Node


class PickStrategy(Enum):
    @staticmethod
    def __pick_all(document: Document) -> List[Node]:
        return document.all_nodes()

    @staticmethod
    def __pick_visible(document: Document) -> List[Node]:
        nodes = document.all_nodes()
        current_node = document.current_node()
        return [node for node in nodes
                if node.is_visible() or node == current_node]

    @staticmethod
    def __pick_current_visibility(document: Document) -> List[Node]:
        nodes = document.all_nodes()
        current_node = document.current_node()
        current_visibility = current_node.is_visible()
        return [node for node in nodes
                if node.is_visible() == current_visibility]

    ALL = __pick_all
    VISIBLE = __pick_visible
    CURRENT_VISIBILITY = __pick_current_visibility
