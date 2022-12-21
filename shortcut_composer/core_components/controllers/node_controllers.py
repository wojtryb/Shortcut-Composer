# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.enums import BlendingMode
from api_krita.pyqt import Text, Colorizer
from ..controller_base import Controller


class NodeBasedController(Controller):
    """Family of controllers which operate on values from active node."""

    def refresh(self):
        """Refresh currently stored active node."""
        self.active_document = Krita.get_active_document()
        self.active_node = self.active_document.active_node


class LayerOpacityController(NodeBasedController):
    """
    Gives access to active layers' `blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get currently active blending mode."""
        return self.active_node.opacity

    def set_value(self, opacity: int) -> None:
        """Set a passed blending mode."""
        if self.active_node.opacity != opacity:
            self.active_node.opacity = opacity
            self.active_document.refresh()

    def get_label(self, value: int) -> Text:
        return Text(f"{value}%", Colorizer.percentage(value))


class LayerBlendingModeController(NodeBasedController):
    """
    Gives access to active layers' `opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get current brush opacity."""
        return self.active_node.blending_mode

    def set_value(self, blending_mode: BlendingMode) -> None:
        """Set passed brush opacity."""
        if self.active_node.blending_mode != blending_mode:
            self.active_node.blending_mode = blending_mode
            self.active_document.refresh()

    def get_label(self, value: BlendingMode) -> Text:
        return Text(value.name[:3], Colorizer.blending_mode(value))


class LayerVisibilityController(NodeBasedController):
    """
    Gives access to active layers' `visibility`.

    - Operates on `bool`
    - Defaults to `True`
    """

    default_value: bool = True

    def get_value(self) -> bool:
        """Get current brush opacity."""
        return self.active_node.visible

    def set_value(self, visibility: bool) -> None:
        """Set passed brush opacity."""
        if self.active_node.visible != visibility:
            self.active_node.visible = visibility
            self.active_document.refresh()
