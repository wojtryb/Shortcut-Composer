from PyQt5.QtWidgets import QWidget, QToolButton, QMainWindow
from krita import Krita as Api, Extension

from .wrappers.document import Document
from .wrappers.canvas import Canvas
from .wrappers.view import View
from .wrappers.cursor import Cursor
from .enums import Tool


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
    def trigger_action(action_name) -> None:
        return Api.instance().action(action_name).trigger()

    @staticmethod
    def get_action_shortcut(action_name: str) -> str:
        return Api.instance().action(action_name).shortcut()

    @staticmethod
    def get_action_state(action_name: str) -> bool:
        return Api.instance().action(action_name).isChecked()

    @staticmethod
    def set_action_state(action_name: str, state: bool) -> None:
        return Api.instance().action(action_name).setChecked(state)

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
        tool = cls._find_my_current_tool()
        return Tool(tool.objectName())

    @classmethod
    def _find_my_current_tool(cls):
        qwindow = Api.instance().activeWindow().qwindow()
        tool_box = cls._find_tool_box(qwindow)
        return cls._find_active_tool(tool_box)

    @staticmethod
    def _find_active_tool(qtoolbox):
        for qobj in qtoolbox.findChildren(QToolButton):
            if qobj.metaObject().className() == "KoToolBoxButton":
                if qobj.isChecked():
                    return qobj

    @staticmethod
    def _find_tool_box(qwindow):
        for qobj in qwindow.findChildren(QWidget):
            if qobj.metaObject().className() == "KoToolBox":
                return qobj
