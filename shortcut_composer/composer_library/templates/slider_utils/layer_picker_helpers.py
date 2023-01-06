from enum import Enum
from typing import Any, List

from ...api import Krita
from ...api.wrappers import Document, Node


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


class CurrentLayerStack:
    def __init__(self, pick_strategy: PickStrategy) -> None:
        self.pick_strategy = pick_strategy
        self.layers = self.get_layers()

    def get_layers(self):
        if document := Krita.get_active_document():
            return self.pick_strategy(document)
        return []

    def __iter__(self):
        return iter(self.layers)

    def __getitem__(self, index: int):
        return self.layers[index]

    def __len__(self):
        self.layers = self.get_layers()
        return len(self.layers)

    def index(self, value: Any):
        return self.layers.index(value)
