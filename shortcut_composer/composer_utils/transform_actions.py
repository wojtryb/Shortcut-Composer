from typing import Dict
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
        self.transform_options: QWidget
        self.apply_button: QPushButton
        self.tool_buttons: Dict[Tool, QToolButton] = {}
        self._initialized = False

    def _ensure_initialized(self, tool: Tool):
        if not self._initialized:
            Tool.TRANSFORM.activate()
            self.transform_options = self._fetch_transform_options()
            self.apply_button = self._fetch_apply_button()
            self._initialized = True

        if tool not in self.tool_buttons:
            self.tool_buttons[tool] = self._fetch_tool_button(tool)

    def _set_mode(self, tool: Tool) -> None:
        self._ensure_initialized(tool)
        button = self.tool_buttons[tool]

        if Krita.active_tool == Tool.TRANSFORM:
            return self._activate_mode_button(button)

        Tool.TRANSFORM.activate()
        Thread(target=self._delayed_click, args=[button], daemon=True).start()

    def _delayed_click(self, button: QToolButton):
        sleep(0.1)
        self._activate_mode_button(button)

    def _activate_mode_button(self, button: QToolButton):
        self.apply_button.click()
        button.click()

    set_perspective = partialmethod(_set_mode, Tool.TRANSFORM_PERSPECTIVE)
    set_warp = partialmethod(_set_mode, Tool.TRANSFORM_WARP)
    set_cage = partialmethod(_set_mode, Tool.TRANSFORM_CAGE)
    set_liquify = partialmethod(_set_mode, Tool.TRANSFORM_LIQUIFY)
    set_mesh = partialmethod(_set_mode, Tool.TRANSFORM_MESH)

    def _fetch_tool_button(self, tool: Tool) -> QToolButton:
        for qobj in self.transform_options.findChildren(QToolButton):
            if qobj.objectName() == self._BUTTONS_MAP[tool]:
                return qobj  # type: ignore
        raise RuntimeError("Couldnt find tool button.")

    def _fetch_apply_button(self) -> QPushButton:
        for qobj in self.transform_options.findChildren(QPushButton):
            qobj: QPushButton
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
