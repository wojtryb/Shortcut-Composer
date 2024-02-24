# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from ..instruction_base import Instruction


class ToggleLayerVisibility(Instruction):
    """Changes the active layer visibility on key press and release."""

    def on_key_press(self) -> None:
        """Change the active layer visibility."""
        document = Krita.get_active_document()
        if document is None:
            raise ValueError("Controller refreshed during initialization")

        self.document = document
        self.affected_node = self.document.active_node
        self.affected_node.toggle_visibility()
        self.document.refresh()

    def on_every_key_release(self, *_) -> None:
        """Change visibility of layer which was active on key press."""
        self.affected_node.toggle_visibility()
        self.document.refresh()


class ToggleVisibilityAbove(Instruction):
    """Changes visibility of layers above on key press and release."""

    def on_key_press(self) -> None:
        """Remember visibility of layers above, and turn them off."""
        document = Krita.get_active_document()
        if document is None:
            raise ValueError("Controller refreshed during initialization")

        self.document = document
        all_nodes = self.document.get_all_nodes(include_collapsed=True)

        top_nodes = all_nodes[all_nodes.index(self.document.active_node)+1:]
        top_nodes = [node for node in top_nodes if not node.is_group_layer]

        self.visible_nodes = [node for node in top_nodes if node.visible]
        for node in self.visible_nodes:
            node.visible = False

        self.document.refresh()

    def on_every_key_release(self) -> None:
        """Recover visibility of layers above from before key press"""
        for node in self.visible_nodes:
            node.visible = True
        self.document.refresh()
