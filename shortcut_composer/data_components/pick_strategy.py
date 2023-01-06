from enum import Enum
from typing import List
from functools import partial

from api_krita.wrappers import Document, Node


class PickStrategy(Enum):

    def _pick_all(document: Document) -> List[Node]:
        return document.get_all_nodes()

    def _pick_current_visibility(document: Document) -> List[Node]:
        nodes = document.get_all_nodes()
        current_visibility = document.active_node.visible
        return [node for node in nodes
                if node.visible == current_visibility]

    def _pick_node_attribute(document: Document, attribute: str) -> List[Node]:
        nodes = document.get_all_nodes()
        return [node for node in nodes
                if getattr(node, attribute) or node == document.active_node]

    ALL = partial(_pick_all)
    VISIBLE = partial(_pick_node_attribute, attribute="visible")
    ANIMATED = partial(_pick_node_attribute, attribute="is_animated")
    CURRENT_VISIBILITY = partial(_pick_current_visibility)
