# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.wrappers import Node
from composer_utils.label import LabelText
from ..controller_base import Controller, NumericController


class DocumentBasedController:
    """Family of controllers which operate on values from active document."""

    def refresh(self) -> None:
        """Refresh currently stored active document."""
        document = Krita.get_active_document()
        if document is None:
            raise ValueError("Controller refreshed during initialization")
        self.document = document


class ActiveLayerController(DocumentBasedController, Controller[Node]):
    """
    Gives access to nodes (layers, groups, masks...) from layer stack.

    - Operates on internal layer objects. Use `CurrentLayerStack(...)`
      to always use current layer stack
    - Does not have a default
    """

    TYPE = Node

    def get_value(self) -> Node | None:
        """Get current node."""
        return self.document.active_node

    def set_value(self, value: Node) -> None:
        """Set passed node as current."""
        self.document.active_node = value

    def get_pretty_name(self, value: Node) -> str:
        """Forward enums' pretty name."""
        return value.name


class TimeController(DocumentBasedController, NumericController):
    """
    Gives access to animation timeline.

    - Operates on `positive integers` representing `frame numbers`
    - Defaults to `0`
    """

    TYPE = int
    DEFAULT_VALUE = 0
    MIN_VALUE = 0
    MAX_VALUE = 10_000
    STEP = 1
    WRAPPING = False
    ADAPTIVE = False

    def get_value(self) -> int:
        """Get current frame on animation timeline."""
        return self.document.current_time

    def set_value(self, value: int) -> None:
        """Set passed frame of animation timeline as active."""
        self.document.current_time = value

    def get_label(self, value: int) -> LabelText:
        """Return LabelText with frame id as string."""
        return LabelText(self.get_pretty_name(value))
