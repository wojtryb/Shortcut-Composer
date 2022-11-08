from dataclasses import dataclass
from typing import List, Protocol

from .node import Node, KritaNode


class KritaDocument(Protocol):
    def activeNode(self) -> KritaNode: ...
    def setActiveNode(self, node: KritaNode): ...
    def topLevelNodes(self) -> List[KritaNode]: ...
    def currentTime(self) -> int: ...
    def setCurrentTime(self, time: int) -> None: ...
    def refreshProjection(self) -> None: ...


@dataclass
class Document:

    document: KritaDocument

    def current_node(self) -> Node:
        return Node(self.document.activeNode())

    def set_current_node(self, node: Node) -> None:
        self.document.setActiveNode(node.node)

    def top_nodes(self) -> List[Node]:
        return [Node(node) for node in self.document.topLevelNodes()]

    def all_nodes(self) -> List[Node]:
        def recursive_search(nodes: List[Node], found_so_far: List[Node]):
            for node in nodes:
                if node.is_group_layer() and not node.is_collapsed():
                    recursive_search(node.child_nodes(), found_so_far)
                found_so_far.append(node)
            return found_so_far
        return recursive_search(self.top_nodes(), [])

    def current_time(self) -> int:
        return self.document.currentTime()

    def set_current_time(self, time: int) -> None:
        self.document.setCurrentTime(time)

    def refresh(self) -> None:
        self.document.refreshProjection()

    def __bool__(self) -> None:
        return bool(self.document)
