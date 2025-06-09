# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.wrappers import Document, Node
from .strategies import PickLayerStrategy


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


class CurrentLayerStack(list):
    """
    List-like container which holds nodes currently on layer stack.

    Provides values that can be set with `ActiveLayerController`.
    Is the only list of nodes that can be specified in configuration.

    Is initialized with `PickLayerStrategy`, which can filter layers
    based on their properties (`default: ALL`).
    """

    def __init__(
        self,
        pick_strategy: PickLayerStrategy = PickLayerStrategy.ALL
    ) -> None:
        self.pick_strategy = pick_strategy

    def get_layers(self) -> list[Node]:
        """Use PickStrategy to fetch and filter nodes from the document."""
        document = Krita.get_active_document()
        if document is None:
            return []

        match self.pick_strategy:
            case PickLayerStrategy.ALL:
                return _pick_all(document)
            case PickLayerStrategy.CURRENT_VISIBILITY:
                return _pick_current_visibility(document)
            case PickLayerStrategy.VISIBLE:
                return _pick_node_attribute(document, "visible")
            case PickLayerStrategy.ANIMATED:
                return _pick_node_attribute(document, "is_animated")
            case PickLayerStrategy.PINNED:
                return _pick_node_attribute(document, "pinned_to_timeline")

        return self.pick_strategy.value(document)

    def __len__(self) -> int:
        """HACK: refresh stack here as handler calls it only once on start."""
        self.clear()
        self.extend(self.get_layers())
        return super().__len__()
