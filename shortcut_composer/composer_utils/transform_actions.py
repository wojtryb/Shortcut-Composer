from typing import Optional, Dict
from time import sleep
from threading import Thread
from functools import partialmethod

from PyQt5.QtWidgets import QWidget, QToolButton, QMainWindow, QPushButton

from api_krita.enums import Tool
from api_krita import Krita


class TransformModeActions:
    """Helper class for finding currently active tool."""

    def __init__(self) -> None:
        """Remember the reference to toolbox krita object."""
        self.transform_options: Optional[QWidget] = None
        self.buttons: Dict[Tool, QToolButton] = {}
        self.apply_button: Optional[QPushButton] = None

    def _late_init(self, tool: Tool):
        if tool not in self.buttons:
            self.buttons[tool] = self._fetch_tool_button(tool)

        if self.apply_button is None:
            self.apply_button = self._fetch_apply_button()

    def _set_button(self, tool: Tool):
        self._late_init(tool)

        if Krita.active_tool == Tool.TRANSFORM:
            self.apply_button.click()
            self.buttons[tool].click()
            return

        Tool.TRANSFORM.activate()
        args = [self.buttons[tool]]
        Thread(target=self._delayed_click, args=args, daemon=True).start()

    def _delayed_click(self, button: QToolButton):
        sleep(0.1)
        self.apply_button.click()
        button.click()

    set_perspective = partialmethod(_set_button, Tool.TRANSFORM_PERSPECTIVE)
    set_warp = partialmethod(_set_button, Tool.TRANSFORM_WARP)
    set_cage = partialmethod(_set_button, Tool.TRANSFORM_CAGE)
    set_liquify = partialmethod(_set_button, Tool.TRANSFORM_LIQUIFY)
    set_mesh = partialmethod(_set_button, Tool.TRANSFORM_MESH)

    def _fetch_tool_button(self, tool: Tool) -> QToolButton:
        Tool.TRANSFORM.activate()
        self.transform_options = self._fetch_transform_options()

        for qobj in self.transform_options.findChildren(QToolButton):
            if qobj.objectName() == self._BUTTONS_MAP[tool]:
                return qobj  # type: ignore
        raise RuntimeError("Couldnt find tool button.")

    def _fetch_apply_button(self) -> QPushButton:
        Tool.TRANSFORM.activate()
        self.transform_options = self._fetch_transform_options()

        for qobj in self.transform_options.findChildren(QPushButton):
            qobj: QPushButton
            print(qobj.objectName(), qobj.text())
            if qobj.text() == "&Apply":
                return qobj  # type: ignore
        raise RuntimeError("Couldnt find apply button.")

    def _fetch_transform_options(self) -> QWidget:
        """Find and return reference to unwrapped options object."""
        searched = "KisToolTransform option widget"
        qwindow = Krita.get_active_qwindow()
        qwindow: QMainWindow
        for qobj in qwindow.findChildren(QWidget):
            if qobj.objectName() == searched:
                return qobj  # type: ignore
        raise RuntimeError("Transform options not found.")

    _BUTTONS_MAP = {
        Tool.TRANSFORM_PERSPECTIVE: "perspectiveTransformButton",
        Tool.TRANSFORM_WARP: "warpButton",
        Tool.TRANSFORM_CAGE: "cageButton",
        Tool.TRANSFORM_LIQUIFY: "liquifyButton",
        Tool.TRANSFORM_MESH: "meshButton",
    }
