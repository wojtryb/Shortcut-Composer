# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.enums import BlendingMode, NodeType
from composer_utils.label import LabelText, LabelTextColorizer
from ..controller_base import Controller, NumericController


class NodeBasedController:
    """Family of controllers which operate on values from active node."""

    def refresh(self) -> None:
        """Refresh currently stored active node."""
        active_document = Krita.get_active_document()
        if active_document is None:
            raise ValueError("Controller refreshed during initialization")
        active_node = active_document.active_node
        if active_node is None:
            raise ValueError("Controller refreshed during initialization")

        self.active_document = active_document
        self.active_node = active_node


class LayerOpacityController(NodeBasedController, NumericController):
    """
    Gives access to active layers' `opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    TYPE = int
    DEFAULT_VALUE = 100
    MIN_VALUE = 0
    MAX_VALUE = 100
    STEP = 1
    WRAPPING = False
    ADAPTIVE = False

    def get_value(self) -> int:
        """Get currently active blending mode."""
        return self.active_node.opacity

    def set_value(self, opacity: int) -> None:
        """Set a passed blending mode."""
        if self.active_node.opacity != opacity:
            self.active_node.opacity = opacity
            self.active_document.refresh()

    def get_label(self, value: int) -> LabelText:
        """Return LabelText with formatted layer opacity."""
        return LabelText(
            value=self.get_pretty_name(value),
            color=LabelTextColorizer.percentage(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the layer opacity like: `100%`"""
        return f"{value}%"


class LayerBlendingModeController(NodeBasedController,
                                  Controller[BlendingMode]):
    """
    Gives access to active layers' `blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    TYPE = BlendingMode
    DEFAULT_VALUE = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get current brush opacity."""
        return self.active_node.blending_mode

    def set_value(self, blending_mode: BlendingMode) -> None:
        """Set passed brush opacity."""
        if self.active_node.blending_mode != blending_mode:
            self.active_node.blending_mode = blending_mode
            self.active_document.refresh()

    def get_label(self, value: BlendingMode) -> LabelText:
        """Return Label of 3 first letters of mode name in correct color."""
        return LabelText(
            value=value.name[:3],
            color=LabelTextColorizer.blending_mode(value))

    def get_pretty_name(self, value: BlendingMode) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


class LayerVisibilityController(NodeBasedController, Controller[bool]):
    """
    Gives access to active layers' `visibility`.

    - Operates on `bool`
    - Defaults to `True`
    """

    TYPE = bool
    DEFAULT_VALUE = True

    def get_value(self) -> bool:
        """Get current brush opacity."""
        return self.active_node.visible

    def set_value(self, visibility: bool) -> None:
        """Set passed brush opacity."""
        if self.active_node.visible != visibility:
            self.active_node.visible = visibility
            self.active_document.refresh()


class CreateLayerWithBlendingController(NodeBasedController,
                                        Controller[BlendingMode]):
    """Creates Paint Layer with set Blending Mode."""

    TYPE = BlendingMode
    DEFAULT_VALUE = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get current layer blending mode."""
        raise NotImplementedError("Can't use this controller to get value")

    def set_value(self, blending_mode: BlendingMode) -> None:
        """Create new paint layer and set blending mode."""
        layer = self.active_document.create_node(
            name=str(blending_mode.value).capitalize() + " Paint Layer",
            node_type=NodeType.PAINT_LAYER)
        layer.blending_mode = blending_mode
        parent = self.active_node.get_parent_node()
        parent.add_child_node(layer, self.active_node)

    def get_label(self, value: BlendingMode) -> LabelText:
        """Return Label of 3 first letters of mode name in correct color."""
        return LabelText(
            value="+" + value.name[:3],
            color=LabelTextColorizer.blending_mode(value))

    def get_pretty_name(self, value: BlendingMode) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name
