from dataclasses import dataclass
from typing import Any


@dataclass
class Node():

    node: Any

    def name(self) -> bool:
        return self.node.name()

    def is_visible(self) -> bool:
        return self.node.visible()

    def set_visible(self, value: bool):
        return self.node.setVisible(value)

    def toggle_visible(self):
        self.set_visible(not self.is_visible())

    def is_group_layer(self) -> bool:
        return self.node.type() == "grouplayer"

    def child_nodes(self):
        return [Node(node) for node in self.node.childNodes()]

    def unique_id(self):
        return self.node.uniqueId()

    def __eq__(self, node: Any):
        if not isinstance(node, Node):
            return False
        return self.unique_id() == node.unique_id()