# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional
from dataclasses import dataclass

from PyQt5.QtGui import QIcon

from api_krita import Krita
from api_krita.enums import Tool, Toggle, TransformMode
from api_krita.pyqt import Text, Colorizer
from api_krita.actions import TransformModeFinder, ColorSamplerOptionsFinder
from ..controller_base import Controller


class ToolController(Controller):
    """
    Gives access to tools from toolbox.

    - Operates on `Tool`
    - Defaults to `Tool.FREEHAND_BRUSH`
    """

    default_value: Tool = Tool.FREEHAND_BRUSH

    @staticmethod
    def get_value() -> Tool:
        """Get currently active tool."""
        return Krita.active_tool

    @staticmethod
    def set_value(value: Tool) -> None:
        """Set a passed tool."""
        Krita.active_tool = value

    def get_label(self, value: Tool) -> QIcon:
        return value.icon


class TransformModeController(Controller):
    """
    Gives access to tools from toolbox.

    - Operates on `TransformMode`
    - Defaults to `TransformMode.FREE`
    """

    default_value: TransformMode = TransformMode.FREE

    def __init__(self) -> None:
        self.button_finder = TransformModeFinder()

    def get_value(self) -> Optional[TransformMode]:
        """Get currently active tool."""
        for mode in TransformMode._member_map_.values():
            self.button_finder.ensure_initialized(mode)  # type: ignore
        return self.button_finder.get_active_mode()

    @staticmethod
    def set_value(value: Optional[TransformMode]) -> None:
        """Set a passed tool."""
        if value is not None:
            value.activate()

    def get_label(self, value: Tool) -> QIcon:
        return value.icon


class ColorSamplerBlendController(Controller):
    """
    Gives access to Blend option in Color Sampler tool.
    """

    default_value: int = 100

    def __init__(self) -> None:
        self.blend_spinbox_finder = ColorSamplerOptionsFinder()

    def get_value(self) -> int:
        """Get current blend percentage."""
        return self.blend_spinbox_finder.get_blend()

    def set_value(self, blend: int) -> None:
        """Set a passed blend percentage."""
        self.blend_spinbox_finder.set_blend(blend)

    def get_label(self, value: int) -> Text:
        return Text(f"{value}%", Colorizer.percentage(value))


@dataclass
class ToggleController(Controller):
    """
    Gives access to picked krita toggle action.

    - Pick an action by providing a specific `Toggle`.
    - Operates on `bool`
    - Defaults to `False`
    """

    toggle: Toggle
    default_value = False

    def get_value(self) -> bool:
        return self.toggle.state

    def set_value(self, value: bool) -> None:
        self.toggle.state = value


@dataclass
class UndoController(Controller):
    """
    Gives access to `undo` and `redo` actions.

    - Operates on `int` representing position on undo stack
    - Starts from `0`
    - Controller remembers its position on undo stack.
    - Setting a value smaller than currently remembered performs `undo`
    - Setting a value greater than currently remembered performs `redo`
    - Each Undo and redo change remembered position by 1
    """

    state = 0

    def get_value(self) -> int:
        """Return remembered position on undo stack"""
        return self.state

    def set_value(self, value: float) -> None:
        """Compares value with remembered position and performs undo/redo."""
        value = round(value)

        if value == self.state:
            return
        elif value > self.state:
            Krita.trigger_action("edit_redo")
            self.state += 1
        else:
            Krita.trigger_action("edit_undo")
            self.state -= 1
