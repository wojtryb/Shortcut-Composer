from typing import Dict
from time import sleep
from threading import Thread
from functools import partialmethod

from PyQt5.QtWidgets import (
    QWidgetAction,
    QToolButton,
    QPushButton,
    QWidget,
)

from api_krita.enums import Tool
from api_krita import Krita


class TransformModeActions:

    def __init__(self) -> None:
        self._finder = self.TransformModeFinder()
        self._actions: Dict[str, QWidgetAction] = {}

    def _set_mode(self, tool: Tool) -> None:
        self._finder.ensure_initialized(tool)

        if Krita.active_tool == Tool.TRANSFORM:
            return self._finder.activate_tool(tool, apply=True)

        Tool.TRANSFORM.activate()
        Thread(target=self._delayed_click, args=[tool], daemon=True).start()

    def _delayed_click(self, tool: Tool):
        sleep(0.1)
        self._finder.activate_tool(tool, apply=False)

    def create_actions(self, window):
        _ACTION_MAP = {
            "Transform tool: free": self.set_free,
            "Transform tool: perspective": self.set_perspective,
            "Transform tool: warp": self.set_warp,
            "Transform tool: cage": self.set_cage,
            "Transform tool: liquify": self.set_liquify,
            "Transform tool: mesh": self.set_mesh,
        }

        for action_name, implementation in _ACTION_MAP.items():
            self._actions[action_name] = Krita.create_action(
                window=window,
                name=action_name,
                callback=implementation
            )

    set_free = partialmethod(_set_mode, Tool.TRANSFORM_FREE)
    set_perspective = partialmethod(_set_mode, Tool.TRANSFORM_PERSPECTIVE)
    set_warp = partialmethod(_set_mode, Tool.TRANSFORM_WARP)
    set_cage = partialmethod(_set_mode, Tool.TRANSFORM_CAGE)
    set_liquify = partialmethod(_set_mode, Tool.TRANSFORM_LIQUIFY)
    set_mesh = partialmethod(_set_mode, Tool.TRANSFORM_MESH)

    class TransformModeFinder:
        def __init__(self) -> None:
            """Remember the reference to toolbox krita object."""
            self.tool_buttons: Dict[Tool, QToolButton] = {}
            self._initialized = False

            self._transform_options: QWidget
            self._apply_button: QPushButton

        def ensure_initialized(self, tool: Tool):
            if not self._initialized:
                Tool.TRANSFORM.activate()
                self._transform_options = self._fetch_transform_options()
                self._apply_button = self._fetch_apply_button()
                self._initialized = True

            if tool not in self.tool_buttons:
                self.tool_buttons[tool] = self._fetch_tool_button(tool)

        def activate_tool(self, tool: Tool, apply: bool):
            if apply:
                self._apply_button.click()
            self.tool_buttons[tool].click()

        def _fetch_tool_button(self, tool: Tool) -> QToolButton:
            for qobj in self._transform_options.findChildren(QToolButton):
                if qobj.objectName() == self._BUTTONS_MAP[tool]:
                    return qobj  # type: ignore
            raise RuntimeError("Couldnt find tool button.")

        def _fetch_apply_button(self) -> QPushButton:
            for qobj in self._transform_options.findChildren(QPushButton):
                if qobj.text() == "&Apply":
                    return qobj  # type: ignore
            raise RuntimeError("Couldnt find apply button.")

        def _fetch_transform_options(self) -> QWidget:
            for qobj in Krita.get_active_qwindow().findChildren(QWidget):
                if qobj.objectName() == "KisToolTransform option widget":
                    return qobj  # type: ignore
            raise RuntimeError("Transform options not found.")

        _BUTTONS_MAP = {
            Tool.TRANSFORM_FREE: "freeTransformButton",
            Tool.TRANSFORM_PERSPECTIVE: "perspectiveTransformButton",
            Tool.TRANSFORM_WARP: "warpButton",
            Tool.TRANSFORM_CAGE: "cageButton",
            Tool.TRANSFORM_LIQUIFY: "liquifyButton",
            Tool.TRANSFORM_MESH: "meshButton",
        }
