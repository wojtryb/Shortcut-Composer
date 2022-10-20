from dataclasses import dataclass
from typing import Any, List

from .node import Node


@dataclass
class Document:

    document: Any

    def current_node(self) -> Node:
        return Node(self.document.activeNode())

    def set_current_node(self, node: Node) -> None:
        self.document.setActiveNode(node.node)

    def top_nodes(self) -> List[Node]:
        return [Node(node) for node in self.document.topLevelNodes()]

    def all_nodes(self):
        def recursive_search(nodes: List[Node], found_so_far: List[Node]):
            for node in nodes:
                if node.is_group_layer():
                    recursive_search(node.child_nodes(), found_so_far)
                found_so_far.append(node)
            return found_so_far
        return recursive_search(self.top_nodes(), [])

    def refresh(self) -> None:
        self.document.refreshProjection()
