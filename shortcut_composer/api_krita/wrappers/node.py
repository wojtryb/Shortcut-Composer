# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import Protocol
from ..enums import BlendingMode


class KritaNode(Protocol):
    """Krita `Node` object API."""

    def addChildNode(self, child: 'KritaNode', above: 'KritaNode') -> bool: ...
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def visible(self) -> bool: ...
    def setVisible(self, visibility: bool) -> None: ...
    def opacity(self) -> int: ...
    def setOpacity(self, opacity: int) -> None: ...
    def blendingMode(self) -> str: ...
    def setBlendingMode(self, mode: str) -> None: ...
    def isPinnedToTimeline(self) -> bool: ...
    def setPinnedToTimeline(self, pinned: bool) -> None: ...
    def type(self) -> str: ...
    def collapsed(self) -> bool: ...
    def setCollapsed(self, value: bool) -> None: ...
    def animated(self) -> bool: ...
    def uniqueId(self) -> str: ...
    def childNodes(self) -> list['KritaNode']: ...
    def parentNode(self) -> 'KritaNode': ...


@dataclass
class Node():
    """Wraps krita `Node` for typing, documentation and PEP8 compatibility."""

    node: KritaNode

    def add_child_node(self, child: 'Node', above: 'Node') -> bool:
        """
        Add the given node in the list of children.

        Parameters:
            child - the node to be added
            above - the node above which this node will be placed

        Returns false if adding the node failed.
        """
        return self.node.addChildNode(child.node, above.node)

    @property
    def name(self) -> str:
        """Settable property with this node's name."""
        return self.node.name()

    @name.setter
    def name(self, new_name: str) -> None:
        """Set name of this node."""
        self.node.setName(new_name)

    @property
    def visible(self) -> bool:
        """Settable property with visibility of this node."""
        return self.node.visible()

    @visible.setter
    def visible(self, value: bool) -> None:
        """Set visibility of this node."""
        self.node.setVisible(value)

    def toggle_visibility(self) -> None:
        """Change visibility of this node to the opposite one."""
        self.visible = not self.visible

    @property
    def opacity(self) -> int:
        """Settable property with opacity of this node."""
        return round(self.node.opacity()/2.55)

    @opacity.setter
    def opacity(self, opacity: int) -> None:
        """Set opacity of this node."""
        self.node.setOpacity(round(2.55*opacity))

    @property
    def blending_mode(self) -> BlendingMode:
        """Settable property with blending_mode of this node."""
        return BlendingMode(self.node.blendingMode())

    @blending_mode.setter
    def blending_mode(self, blending_mode: BlendingMode) -> None:
        """Set blending_mode of this node."""
        self.node.setBlendingMode(blending_mode.value)

    @property
    def pinned_to_timeline(self) -> bool:
        """Settable property of node being pinned to timeline."""
        return self.node.isPinnedToTimeline()

    @pinned_to_timeline.setter
    def pinned_to_timeline(self, pinned_to_timeline: bool) -> None:
        """Set pinned_to_timeline property of this node."""
        self.node.setPinnedToTimeline(pinned_to_timeline)

    @property
    def collapsed(self) -> bool:
        """Settable property telling whether this node is collapsed."""
        return self.node.collapsed()

    @collapsed.setter
    def collapsed(self, value: bool) -> None:
        """Change collapsed state of this node."""
        self.node.setCollapsed(value)

    @property
    def is_group_layer(self) -> bool:
        """Read-only property telling if this node is a group."""
        return self.node.type() == "grouplayer"

    @property
    def is_animated(self) -> bool:
        """Read-only property telling if this node has animation frames."""
        return self.node.animated()

    def get_child_nodes(self) -> list['Node']:
        """Return a list of wrapped Nodes that are children of this one."""
        return [Node(node) for node in self.node.childNodes()]

    def get_parent_node(self) -> 'Node':
        """Return wrapped Node being a parent of this node."""
        return Node(self.node.parentNode())

    @property
    def unique_id(self) -> str:
        """Read-only property holding unique ID of a node."""
        return self.node.uniqueId()

    def __eq__(self, node: 'Node') -> bool:
        """Two objects are the same node, when their unique IDs matches."""
        if not isinstance(node, Node):
            return False
        return self.unique_id == node.unique_id
