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

    @staticmethod
    def get_active_view() -> View:
        return View(Api.instance().activeWindow().activeView())

    @classmethod
    def get_cursor(cls) -> Cursor:
        qwin = cls.get_active_qwindow()
        return Cursor(qwin)

    @staticmethod
    def get_active_document() -> Document:
        return Document(Api.instance().activeDocument())

    @staticmethod
    def get_active_canvas() -> Canvas:
        return Canvas(Api.instance().activeWindow().activeView().canvas())

    @staticmethod
    def trigger_action(action_name: str) -> None:
        return Api.instance().action(action_name).trigger()

    @staticmethod
    def get_action_shortcut(action_name: str) -> QKeySequence:
        return Api.instance().action(action_name).shortcut()

    @staticmethod
    def get_toggle_state(toggle: Toggle) -> bool:
        return Api.instance().action(toggle.value).isChecked()

    @staticmethod
    def set_toggle_state(toggle: Toggle, state: bool) -> None:
        return Api.instance().action(toggle.value).setChecked(state)

    @staticmethod
    def get_presets() -> dict:
        return Api.instance().resources('preset')

    @staticmethod
    def get_active_qwindow() -> QMainWindow:
        return Api.instance().activeWindow().qwindow()

    @staticmethod
    def add_extension(extension: Extension) -> None:
        Api.instance().addExtension(extension(Api.instance()))

    @classmethod
    def get_current_tool(cls) -> Tool:
        if not hasattr(cls, "tool_finder"):
            cls.tool_finder = cls.ToolFinder()
        tool = cls.tool_finder.find_my_current_tool()
        return Tool(tool.objectName())

    class ToolFinder:
        def __init__(self) -> None:
            self.toolbox = self._find_toolbox()

        @classmethod
        def _find_toolbox(cls):
            qwindow = Api.instance().activeWindow().qwindow()
            for qobj in qwindow.findChildren(QWidget):
                if qobj.metaObject().className() == "KoToolBox":
                    return qobj

        def find_my_current_tool(self):
            for qobj in self.toolbox.findChildren(QToolButton):
                if qobj.metaObject().className() == "KoToolBoxButton":
                    if qobj.isChecked():
                        return qobj
