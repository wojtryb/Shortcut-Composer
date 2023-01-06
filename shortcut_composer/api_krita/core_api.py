from typing import Any

from PyQt5.QtWidgets import QWidget, QToolButton, QMainWindow
from PyQt5.QtGui import QKeySequence
from krita import Krita as Api, Extension

from .wrappers import (
    Document,
    Canvas,
    Cursor,
    View,
)
from .enums import Tool, Toggle


class Krita:
    """Wraps krita API for typing, documentation and PEP8 compatibility."""

    @staticmethod
    def get_active_view() -> View:
        """Return wrapper of krita `View`."""
        return View(Api.instance().activeWindow().activeView())

    @classmethod
    def get_cursor(cls) -> Cursor:
        """Return wrapper of krita `Cursor`. Don't use on plugin init phase."""
        qwin = cls.get_active_qwindow()
        return Cursor(qwin)

    @staticmethod
    def get_active_document() -> Document:
        """Return wrapper of krita `Document`."""
        return Document(Api.instance().activeDocument())

    @staticmethod
    def get_active_canvas() -> Canvas:
        """Return wrapper of krita `Canvas`."""
        return Canvas(Api.instance().activeWindow().activeView().canvas())

    @staticmethod
    def trigger_action(action_name: str) -> None:
        """Trigger internal krita action called `action_name`."""
        return Api.instance().action(action_name).trigger()

    @staticmethod
    def get_action_shortcut(action_name: str) -> QKeySequence:
        """Return shortcut of krita action called `action_name`."""
        return Api.instance().action(action_name).shortcut()

    @staticmethod
    def get_toggle_state(toggle: Toggle) -> bool:
        """Return state of checkable krita action called `action_name`."""
        return Api.instance().action(toggle.value).isChecked()

    @staticmethod
    def set_toggle_state(toggle: Toggle, state: bool) -> None:
        """Set state of checkable krita action (toggle) by its enum."""
        return Api.instance().action(toggle.value).setChecked(state)

    @staticmethod
    def get_presets() -> dict:
        """Return a list of unwrapped preset objects"""
        return Api.instance().resources('preset')

    @staticmethod
    def get_active_qwindow() -> QMainWindow:
        """Return qt window of krita. Don't use on plugin init phase."""
        return Api.instance().activeWindow().qwindow()

    @staticmethod
    def add_extension(extension: Extension) -> None:
        """Add extension/plugin/add-on to krita."""
        Api.instance().addExtension(extension(Api.instance()))

    @classmethod
    def get_current_tool(cls) -> Tool:
        """Return enum of currently active tool."""
        if not hasattr(cls, "tool_finder"):
            cls.tool_finder = cls.ToolFinder()
        current_tool_name = cls.tool_finder.find_current_tool_name()
        return Tool(current_tool_name)

    class ToolFinder:
        """Helper class for finding currently active tool."""

        def __init__(self) -> None:
            """Remember the reference to unwrapper toolbox object."""
            self.toolbox = self._find_toolbox()

        @classmethod
        def _find_toolbox(cls) -> Any:
            """Find and return reference to unwrapper toolbox object."""
            qwindow = Api.instance().activeWindow().qwindow()
            for qobj in qwindow.findChildren(QWidget):
                if qobj.metaObject().className() == "KoToolBox":
                    return qobj

        def find_current_tool_name(self) -> str:
            """Find and return name of currently active tool."""
            for qobj in self.toolbox.findChildren(QToolButton):
                if qobj.metaObject().className() == "KoToolBoxButton":
                    if qobj.isChecked():
                        return qobj.objectName()
            raise RuntimeError("No active tool found.")
