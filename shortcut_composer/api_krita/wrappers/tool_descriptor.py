# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from PyQt5.QtWidgets import QWidget, QToolButton

from ..enums import Tool


class ToolDescriptor:
    """Allows setting active `Tool`, as if it was a instance variable."""

    _tool_finder: 'ToolFinder'

    def __init__(self) -> None:
        self.instance = Api.instance()

    def __set__(self, _, tool_enum: Tool) -> None:
        """Set active tool by triggering related action."""
        tool_enum.activate()

    def __get__(self, *_) -> Tool:
        """
        Return enum of an active tool.

        First call creates a new ToolFinder needed to fetch a tool.
        It is then stored as attribute, as it's creation in relatively
        heavy.

        Further calls will reuse the same ToolFinder instance.
        ToolFinder cannot be created in __init__, as krita is not fully
        initialized at this point.
        """
        if not hasattr(self, "_tool_finder"):
            self._tool_finder = self.ToolFinder()
        current_tool_name = self._tool_finder.find_active_tool_name()
        return Tool(current_tool_name)

    class ToolFinder:
        """Helper class for finding currently active tool."""

        def __init__(self) -> None:
            """Remember the reference to toolbox krita object."""
            self.instance = Api.instance()
            self.toolbox: QWidget

        def find_active_tool_name(self) -> str:
            """Find and return name of currently active tool."""
            self._ensure_toolbox()
            for q_obj in self.toolbox.findChildren(QToolButton):
                if q_obj.metaObject().className() == "KoToolBoxButton":
                    if q_obj.isChecked():
                        return q_obj.objectName()
            raise RuntimeError("No active tool found.")

        def _ensure_toolbox(self):
            """Fetch toolbox if it was not fetched or got deleted."""
            try:
                self.toolbox.size()
            except (RuntimeError, AttributeError):
                self.toolbox = self._init_toolbox()

        def _init_toolbox(self) -> QWidget:
            """Find and return reference to unwrapped toolbox object."""
            qwindow = self.instance.activeWindow().qwindow()
            for q_obj in qwindow.findChildren(QWidget):
                if q_obj.metaObject().className() == "KoToolBox":
                    return q_obj
            raise RuntimeError("Toolbox not found.")
