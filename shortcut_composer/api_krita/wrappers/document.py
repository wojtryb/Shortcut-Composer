# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import List, Protocol

from .node import Node, KritaNode


class KritaDocument(Protocol):
    """Krita `Document` object API."""

    def activeNode(self) -> KritaNode: ...
    def setActiveNode(self, node: KritaNode): ...
    def topLevelNodes(self) -> List[KritaNode]: ...
    def resolution(self) -> int: ...
    def currentTime(self) -> int: ...
    def setCurrentTime(self, time: int) -> None: ...
    def refreshProjection(self) -> None: ...


@dataclass
class Document:
    """Wraps krita `Document` for typing, docs and PEP8 compatibility."""

    document: KritaDocument

    @property
    def active_node(self) -> Node:
        """Settable property with this `Document`'s active `Node`."""
        return Node(self.document.activeNode())

    @active_node.setter
    def active_node(self, node: Node) -> None:
        """Set active `Node`."""
        self.document.setActiveNode(node.node)

    @property
    def current_time(self) -> int:
        """Settable property with this `Document`'s current frame number."""
        return self.document.currentTime()

    @current_time.setter
    def current_time(self, time: int) -> None:
        """Set current time using frame number"""
        self.document.setCurrentTime(time)

    def get_top_nodes(self) -> List[Node]:
        """Return a list of `Nodes` without a parent."""
        return [Node(node) for node in self.document.topLevelNodes()]

    def get_all_nodes(self) -> List[Node]:
        """Return a list of all `Nodes` in this document bottom to top."""
        def recursive_search(nodes: List[Node], found_so_far: List[Node]):
            for node in nodes:
                if node.is_group_layer and not node.collapsed:
                    recursive_search(node.get_child_nodes(), found_so_far)
                found_so_far.append(node)
            return found_so_far
        return recursive_search(self.get_top_nodes(), [])

    @property
    def dpi(self):
        """Return dpi (dot per inch) of the document."""
        return self.document.resolution()

    def refresh(self) -> None:
        """Refresh OpenGL projection of this document."""
        self.document.refreshProjection()

    def __bool__(self) -> bool:
        """Return true if the wrapped document exists."""
        return bool(self.document)
