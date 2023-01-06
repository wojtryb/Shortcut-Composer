from typing import Dict, Literal
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

TransformMode = Literal[
    Tool.TRANSFORM_FREE,
    Tool.TRANSFORM_PERSPECTIVE,
    Tool.TRANSFORM_WARP,
    Tool.TRANSFORM_CAGE,
    Tool.TRANSFORM_LIQUIFY,
    Tool.TRANSFORM_MESH,
]


class TransformModeActions:
    """
    Divides transform tool into separate tools.

    Tools are available as krita actions, but not added to the toolbar.
    """

    def __init__(self) -> None:
        self._finder = self.TransformModeFinder()
        self._actions: Dict[str, QWidgetAction] = {}

    def _set_mode(self, mode: TransformMode) -> None:
        """Set a passed mode. Implementation of the new krita tool."""
        self._finder.ensure_initialized(mode)

        if Krita.active_tool == Tool.TRANSFORM:
            return self._finder.activate_mode(mode, apply=True)

        Tool.TRANSFORM.activate()
        Thread(target=self._delayed_click, args=[mode], daemon=True).start()

    def _delayed_click(self, mode: TransformMode):
        """Activate a mode after a small delay, so that krita notices it."""
        sleep(0.1)
        self._finder.activate_mode(mode, apply=False)

    def create_actions(self, window):
        """Create krita actions which activate new tools."""
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
        """
        Helper class for finding components related to transform modes.

        Stores elements of krita needed to control transform modes:
        - Widget transform tool options
        - Buttons of every transform modes from the tool options widget
        - Button used to apply the changes of transform tool

        As the widget do not exist during plugin intialization phase,
        fetching the elements needs to happen at runtime.
        """

        def __init__(self) -> None:
            self._mode_buttons: Dict[TransformMode, QToolButton] = {}
            self._initialized = False

            self._transform_options: QWidget
            self._apply_button: QPushButton

        def ensure_initialized(self, mode: TransformMode):
            """Fetch widget, apply and mode buttons if not done already."""
            if not self._initialized:
                Tool.TRANSFORM.activate()
                self._transform_options = self._fetch_transform_options()
                self._apply_button = self._fetch_apply_button()
                self._initialized = True

            if mode not in self._mode_buttons:
                self._mode_buttons[mode] = self._fetch_mode_button(mode)

        def activate_mode(self, mode: TransformMode, apply: bool):
            """Apply transform if requested and activate given mode."""
            if apply:
                self._apply_button.click()
            self._mode_buttons[mode].click()

        def _fetch_transform_options(self) -> QWidget:
            """Fetch widget with transform tool options."""
            for qobj in Krita.get_active_qwindow().findChildren(QWidget):
                if qobj.objectName() == "KisToolTransform option widget":
                    return qobj  # type: ignore
            raise RuntimeError("Transform options not found.")

        def _fetch_mode_button(self, mode: TransformMode) -> QToolButton:
            """Fetch a button that activates a given mode."""
            for qobj in self._transform_options.findChildren(QToolButton):
                if qobj.objectName() == self._BUTTONS_MAP[mode]:
                    return qobj  # type: ignore
            raise RuntimeError(f"Could not find the {mode.name} button.")

        def _fetch_apply_button(self) -> QPushButton:
            """Fetch a button that applies the transformation."""
            for qobj in self._transform_options.findChildren(QPushButton):
                if qobj.text() == "&Apply":
                    return qobj  # type: ignore
            raise RuntimeError("Could not find the apply button.")

        _BUTTONS_MAP = {
            Tool.TRANSFORM_FREE: "freeTransformButton",
            Tool.TRANSFORM_PERSPECTIVE: "perspectiveTransformButton",
            Tool.TRANSFORM_WARP: "warpButton",
            Tool.TRANSFORM_CAGE: "cageButton",
            Tool.TRANSFORM_LIQUIFY: "liquifyButton",
            Tool.TRANSFORM_MESH: "meshButton",
        }
        """Maps the TransformMode Tools to their buttons from the widget."""
