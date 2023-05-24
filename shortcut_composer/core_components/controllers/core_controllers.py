# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union, NoReturn
from dataclasses import dataclass

from PyQt5.QtGui import QIcon

from api_krita import Krita
from api_krita.pyqt import Text
from api_krita.enums import Action, Tool, Toggle, TransformMode
from api_krita.actions import TransformModeFinder
from ..controller_base import Controller


class ToolController(Controller[Tool]):
    """
    Gives access to tools from toolbox.

    - Operates on `Tool`
    - Defaults to `Tool.FREEHAND_BRUSH`
    """

    TYPE = Tool
    DEFAULT_VALUE: Tool = Tool.FREEHAND_BRUSH

    @staticmethod
    def get_value() -> Tool:
        """Get currently active tool."""
        return Krita.active_tool

    @staticmethod
    def set_value(value: Tool) -> None:
        """Set a passed tool."""
        Krita.active_tool = value

    def get_label(self, value: Tool) -> QIcon:
        """Forward the tools' icon."""
        return value.icon

    def get_pretty_name(self, value: Tool) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


class ActionController(Controller[Action]):
    """
    Gives access to krita actions.

    - Operates on `Action`
    - Does not have a default value.
    """

    TYPE = Action

    @staticmethod
    def get_value() -> NoReturn:
        """Get currently active tool."""
        raise NotImplementedError()

    @staticmethod
    def set_value(value: Action) -> None:
        """Set a passed tool."""
        value.activate()

    def get_label(self, value: Tool) -> Union[QIcon, Text]:
        """Forward the tools' icon."""
        icon = value.icon
        if not icon.isNull():
            return value.icon
        return Text(value.name[:3])

    def get_pretty_name(self, value: Action) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


class TransformModeController(Controller[TransformMode]):
    """
    Gives access to tools from toolbox.

    - Operates on `TransformMode`
    - Defaults to `TransformMode.FREE`
    """

    TYPE = TransformMode
    DEFAULT_VALUE: TransformMode = TransformMode.FREE

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
        """Forward the transform mode icon."""
        return value.icon

    def get_pretty_name(self, value: Tool) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


@dataclass
class ToggleController(Controller[bool]):
    """
    Gives access to picked krita toggle action.

    - Pick an action by providing a specific `Toggle`.
    - Operates on `bool`
    - Defaults to `False`
    """

    toggle: Toggle
    TYPE = bool
    DEFAULT_VALUE = False

    def get_value(self) -> bool:
        """Return whether the toggle action is on."""
        return self.toggle.state

    def set_value(self, value: bool) -> None:
        """Set the toggle action on or off using a bool."""
        self.toggle.state = value

    def get_pretty_name(self, value: Tool) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


class UndoController(Controller[float]):
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
    TYPE = float
    DEFAULT_VALUE = 0

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
