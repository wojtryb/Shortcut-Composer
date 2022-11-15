from dataclasses import dataclass
from typing import List, Protocol


class KritaNode(Protocol):
    def name(self) -> str: ...
    def visible(self) -> bool: ...
    def setVisible(self, visibility: bool) -> None: ...
    def type(self) -> str: ...
    def collapsed(self) -> bool: ...
    def setCollapsed(self, value: bool) -> None: ...
    def animated(self) -> bool: ...
    def uniqueId(self) -> str: ...
    def childNodes(self) -> List['KritaNode']: ...
    def parentNode(self) -> 'KritaNode': ...


@dataclass
class Node():

    node: KritaNode

    @property
    def name(self) -> str:
        return self.node.name()

    @property
    def visible(self) -> bool:
        return self.node.visible()

    @visible.setter
    def visible(self, value: bool) -> None:
        self.node.setVisible(value)

    def toggle_visility(self) -> None:
        self.visible = not self.visible

    @property
    def collapsed(self) -> bool:
        return self.node.collapsed()

    @collapsed.setter
    def collapsed(self, value: bool) -> None:
        self.node.setCollapsed(value)

    @property
    def is_group_layer(self) -> bool:
        return self.node.type() == "grouplayer"

    @property
    def is_animated(self) -> bool:
        return self.node.animated()

    def get_child_nodes(self) -> List['Node']:
        return [Node(node) for node in self.node.childNodes()]

    def get_parent_node(self) -> 'Node':
        return Node(self.node.parentNode())

    @property
    def unique_id(self) -> str:
        return self.node.uniqueId()

    def __eq__(self, node: 'Node') -> bool:
        if not isinstance(node, Node):
            return False
        return self.unique_id == node.unique_id
