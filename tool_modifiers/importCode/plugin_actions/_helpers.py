# courtesy of AkiR
# https://krita-artists.org/t/discovering-which-toolbox-tool-is-active/10580

from krita import Krita
from PyQt5.QtWidgets import QWidget, QToolButton


def get_current_tool_name() -> str:
    tool = _find_my_current_tool()
    return tool.objectName()


def _find_my_current_tool():
    qwindow = Krita.instance().activeWindow().qwindow()
    tool_box = _find_tool_box(qwindow)
    return _find_active_tool(tool_box)


def _find_active_tool(qtoolbox):
    for qobj in qtoolbox.findChildren(QToolButton):
        if qobj.metaObject().className() == "KoToolBoxButton":
            if qobj.isChecked():
                return qobj


def _find_tool_box(qwindow):
    for qobj in qwindow.findChildren(QWidget):
        if qobj.metaObject().className() == "KoToolBox":
            return qobj
