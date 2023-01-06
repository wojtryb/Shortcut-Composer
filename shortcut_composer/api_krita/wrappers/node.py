from dataclasses import dataclass
from typing import List, Protocol


class KritaNode(Protocol):
    def name(self) -> str: ...
    def visible(self) -> bool: ...
    def setVisible(self, visibility: bool) -> None: ...
    def type(self) -> str: ...
    def collapsed(self) -> bool: ...
    def animated(self) -> bool: ...
    def uniqueId(self) -> str: ...
    def childNodes(self) -> List['KritaNode']: ...


@dataclass
class Node():

    node: KritaNode

    def name(self) -> str:
        return self.node.name()

    def is_visible(self) -> bool:
        return self.node.visible()

    def set_visible(self, value: bool) -> None:
        return self.node.setVisible(value)

    def toggle_visible(self) -> None:
        self.set_visible(not self.is_visible())

    def is_group_layer(self) -> bool:
        return self.node.type() == "grouplayer"

    def is_collapsed(self) -> bool:
        return self.node.collapsed()

    def is_animated(self) -> bool:
        return self.node.animated()

    def child_nodes(self) -> List['Node']:
        return [Node(node) for node in self.node.childNodes()]

    def unique_id(self) -> str:
        return self.node.uniqueId()

    def __eq__(self, node: 'Node') -> bool:
        if not isinstance(node, Node):
            return False
        return self.unique_id() == node.unique_id()
