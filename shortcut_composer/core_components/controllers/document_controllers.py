# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.wrappers import Node
from api_krita.pyqt import Text
from ..controller_base import Controller


class DocumentBasedController(Controller):
    """Family of controllers which operate on values from active document."""

    def refresh(self):
        """Refresh currently stored active document."""
        self.document = Krita.get_active_document()


class ActiveLayerController(DocumentBasedController):
    """
    Gives access to nodes (layers, groups, masks...) from layer stack.

    - Operates on internal layer objects. Use `CurrentLayerStack(...)`
      to always use current layer stack
    - Does not have a default
    """

    def get_value(self) -> Node:
        """Get current node."""
        return self.document.active_node

    def set_value(self, value: Node) -> None:
        """Set passed node as current."""
        self.document.active_node = value


class TimeController(DocumentBasedController):
    """
    Gives access to animation timeline.

    - Operates on `positive integers` representing `frame numbers`
    - Defaults to `0`
    """

    default_value = 0

    def get_value(self) -> int:
        return self.document.current_time

    def set_value(self, value: int) -> None:
        self.document.current_time = value

    def get_label(self, value: int) -> Text:
        return Text(str(value))
