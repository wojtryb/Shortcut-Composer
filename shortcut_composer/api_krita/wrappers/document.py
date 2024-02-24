# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import Protocol

from PyQt5.QtCore import QByteArray

from ..enums import NodeType
from .node import Node, KritaNode


class KritaDocument(Protocol):
    """Krita `Document` object API."""

    def activeNode(self) -> KritaNode: ...
    def setActiveNode(self, node: KritaNode): ...
    def createNode(self, name: str, node_type: str) -> KritaNode: ...
    def topLevelNodes(self) -> list[KritaNode]: ...
    def resolution(self) -> int: ...
    def currentTime(self) -> int: ...
    def setCurrentTime(self, time: int) -> None: ...
    def refreshProjection(self) -> None: ...
    def annotation(self, type: str) -> QByteArray: ...
    def annotationTypes(self) -> list[str]: ...

    def setAnnotation(
        self,
        type: str,
        description: str,
        annotation: bytes) -> None: ...


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

    def create_node(self, name: str, node_type: NodeType) -> Node:
        """
        Create a Node.

        IMPORTANT: Created node must be then added to node tree to be
        usable from Krita. For example with add_child_node() method of
        Node Class.

        When relevant, the new Node will have the color space of the
        image by default; that can be changed with Node::setColorSpace.

        The settings and selections for relevant layer and mask types
        can also be set after the Node has been created.
        """
        return Node(self.document.createNode(name, node_type.value))

    @property
    def current_time(self) -> int:
        """Settable property with this `Document`'s current frame number."""
        return self.document.currentTime()

    @current_time.setter
    def current_time(self, time: int) -> None:
        """Set current time using frame number"""
        self.document.setCurrentTime(round(time))

    def get_top_nodes(self) -> list[Node]:
        """Return a list of `Nodes` without a parent."""
        return [Node(node) for node in self.document.topLevelNodes()]

    def get_all_nodes(self, include_collapsed: bool = False) -> list[Node]:
        """Return a list of all `Nodes` in this document bottom to top."""
        def recursive_search(nodes: list[Node], found_so_far: list[Node]):
            for node in nodes:
                if include_collapsed or not node.collapsed:
                    recursive_search(node.get_child_nodes(), found_so_far)
                found_so_far.append(node)
            return found_so_far
        return recursive_search(self.get_top_nodes(), [])

    @property
    def dpi(self) -> int:
        """Return dpi (dot per inch) of the document."""
        return self.document.resolution()

    def refresh(self) -> None:
        """Refresh OpenGL projection of this document."""
        self.document.refreshProjection()

    def read_annotation(self, name: str) -> str:
        """Read annotation from .kra document parsed as string."""
        return self.document.annotation(name).data().decode(encoding="utf-8")

    def write_annotation(self, name: str, description: str, value: str):
        """Write annotation to .kra document."""
        self.document.setAnnotation(
            name,
            description,
            value.encode(encoding="utf-8"))

    def contains_annotation(self, name: str) -> bool:
        """Return if annotation of given name is stored in .kra."""
        return name in self.document.annotationTypes()
