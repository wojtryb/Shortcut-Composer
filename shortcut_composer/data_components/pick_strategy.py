# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from functools import partial

from api_krita.wrappers import Document, Node


def _pick_all(document: Document) -> list[Node]:
    """Pick all nodes from document as list without group hierarchy"""
    return document.get_all_nodes(include_collapsed=False)


def _pick_current_visibility(document: Document) -> list[Node]:
    """Pick nodes from document that has the same visibility as active one."""
    nodes = document.get_all_nodes(include_collapsed=False)
    current_visibility = document.active_node.visible
    return [node for node in nodes
            if node.visible == current_visibility]


def _pick_node_attribute(document: Document, attribute: str) -> list[Node]:
    """Pick nodes from document based on a single attribute."""
    nodes = document.get_all_nodes(include_collapsed=False)
    return [node for node in nodes
            if getattr(node, attribute) or node == document.active_node]


class PickStrategy(Enum):
    """
    Specifies what layers to pick when scrolling through layers.

    Available strategies are:
    - `ALL`               -- picks all the nodes in the stack
                             (layers, groups, masks...).
    - `VISIBLE`           -- picks active node and all the nodes that are
                             visible.
    - `CURRENT_VISIBILITY`-- picks all the nodes with the same visibility
                             as the active node.
    - `ANIMATED`          -- picks active node and all the nodes that
                             have animation frames.
    - `PINNED`            -- picks active node and all the nodes that
                             are pinned to timeline.


    ### Usage Example:

    ```python
    PickStrategy.CURRENT_VISIBILITY
    ```
    """
    ALL = partial(_pick_all)
    VISIBLE = partial(_pick_node_attribute, attribute="visible")
    CURRENT_VISIBILITY = partial(_pick_current_visibility)
    ANIMATED = partial(_pick_node_attribute, attribute="is_animated")
    PINNED = partial(_pick_node_attribute, attribute="pinned_to_timeline")
