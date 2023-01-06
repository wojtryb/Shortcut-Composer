from typing import Any

from PyQt5.QtWidgets import QWidget, QToolButton
from krita import Krita as Api

from ..enums import Tool


class ToolDescriptor:

    _tool_finder: 'ToolFinder'

    def __init__(self):
        self.instance = Api.instance()

    def __set__(self, _, tool_enum: Tool):
        self.instance.action(tool_enum.value).trigger()

    def __get__(self, *_) -> Tool:
        """Return enum of currently active tool."""
        if not hasattr(self, "_tool_finder"):
            self._tool_finder = self.ToolFinder()
        current_tool_name = self._tool_finder.find_active_tool_name()
        return Tool(current_tool_name)

    class ToolFinder:
        """Helper class for finding currently active tool."""

        def __init__(self) -> None:
            """Remember the reference to unwrapper toolbox object."""
            self.instance = Api.instance()
            self.toolbox = self.__init_toolbox()

        def find_active_tool_name(self) -> str:
            """Find and return name of currently active tool."""
            for qobj in self.toolbox.findChildren(QToolButton):
                if qobj.metaObject().className() == "KoToolBoxButton":
                    if qobj.isChecked():
                        return qobj.objectName()
            raise RuntimeError("No active tool found.")

        def __init_toolbox(self) -> Any:
            """Find and return reference to unwrapper toolbox object."""
            qwindow = self.instance.activeWindow().qwindow()
            for qobj in qwindow.findChildren(QWidget):
                if qobj.metaObject().className() == "KoToolBox":
                    return qobj
