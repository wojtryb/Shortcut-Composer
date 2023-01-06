from PyQt5.QtWidgets import QWidget, QToolButton
from krita import Krita as Api

from ..enums import Tool


class ToolDescriptor:
    """Allows setting active `Tool`, as if it was a instance variable."""

    _tool_finder: 'ToolFinder'

    def __init__(self):
        self.instance = Api.instance()

    def __set__(self, _, tool_enum: Tool):
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
            self.toolbox = self.__init_toolbox()

        def find_active_tool_name(self) -> str:
            """Find and return name of currently active tool."""
            for qobj in self.toolbox.findChildren(QToolButton):
                if qobj.metaObject().className() == "KoToolBoxButton":
                    if qobj.isChecked():
                        return qobj.objectName()
            raise RuntimeError("No active tool found.")

        def __init_toolbox(self) -> QWidget:
            """Find and return reference to unwrapped toolbox object."""
            qwindow = self.instance.activeWindow().qwindow()
            for qobj in qwindow.findChildren(QWidget):
                if qobj.metaObject().className() == "KoToolBox":
                    return qobj
            raise RuntimeError("Toolbox not found.")
