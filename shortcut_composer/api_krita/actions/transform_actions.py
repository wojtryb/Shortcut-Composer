# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import partial, partialmethod

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QWidgetAction,
    QToolButton,
    QPushButton,
    QWidget)

from ..enums import Tool, TransformMode
from ..core_api import KritaInstance

Krita = KritaInstance()


class TransformModeActions:
    """
    Divides transform tool into separate tools.

    Tools are available as krita actions, but not added to the toolbar.
    """

    def __init__(self, window) -> None:
        self._finder = TransformModeFinder()
        self._actions: dict[TransformMode, QWidgetAction] = {}
        self._create_actions(window)

    def _create_actions(self, window) -> None:
        """Create krita actions which activate new tools."""
        _ACTION_MAP = {
            TransformMode.FREE: self.set_free,
            TransformMode.PERSPECTIVE: self.set_perspective,
            TransformMode.WARP: self.set_warp,
            TransformMode.CAGE: self.set_cage,
            TransformMode.LIQUIFY: self.set_liquify,
            TransformMode.MESH: self.set_mesh}

        for action, implementation in _ACTION_MAP.items():
            self._actions[action] = Krita.create_action(
                window=window,
                name=action.value,
                callback=implementation)

    def _set_mode(self, mode: TransformMode) -> None:
        """Set a passed mode. Implementation of the new krita tool."""
        self._finder.ensure_initialized(mode)

        if Krita.active_tool == Tool.TRANSFORM:
            return self._finder.activate_mode(mode, apply=True)

        Tool.TRANSFORM.activate()
        self._delayed_click(mode)

    def _delayed_click(self, mode: TransformMode) -> None:
        """Trigger an mode after short period of time to workaround a bug."""
        method = partial(self._finder.activate_mode, mode=mode, apply=False)
        QTimer.singleShot(40, method)

    set_free = partialmethod(_set_mode, TransformMode.FREE)
    set_perspective = partialmethod(_set_mode, TransformMode.PERSPECTIVE)
    set_warp = partialmethod(_set_mode, TransformMode.WARP)
    set_cage = partialmethod(_set_mode, TransformMode.CAGE)
    set_liquify = partialmethod(_set_mode, TransformMode.LIQUIFY)
    set_mesh = partialmethod(_set_mode, TransformMode.MESH)


class TransformModeFinder:
    """
    Helper class for finding components related to transform modes.

    Stores elements of krita needed to control transform modes:
    - Widget transform tool options
    - Buttons of every transform modes from the tool options widget
    - Button used to apply the changes of transform tool

    As the widget do not exist during plugin initialization phase,
    fetching the elements needs to happen at runtime. If wrappers get
    deleted by C++, the fetching may need to be done again.
    """

    def __init__(self) -> None:
        self._mode_buttons: dict[TransformMode, QToolButton] = {}
        self._transform_options: QWidget
        self._apply_button: QPushButton

    def ensure_initialized(self, mode: TransformMode) -> None:
        """Fetch widget, apply and mode buttons if not done already."""
        try:
            self._transform_options.size()
            self._apply_button.size()
        except (RuntimeError, AttributeError):
            last_tool = Krita.active_tool
            Krita.active_tool = Tool.TRANSFORM
            self._transform_options = self._fetch_transform_options()
            self._apply_button = self._fetch_apply_button()
            Krita.active_tool = last_tool

        try:
            self._mode_buttons[mode].size()
        except (RuntimeError, KeyError):
            self._mode_buttons[mode] = self._fetch_mode_button(mode)

    def activate_mode(self, mode: TransformMode, apply: bool) -> None:
        """Apply transform if requested and activate given mode."""
        if apply:
            self._apply_button.click()
        self._mode_buttons[mode].click()

    def get_active_mode(self) -> TransformMode | None:
        for mode, button in self._mode_buttons.items():
            if button.isChecked():
                return mode
        return None

    def _fetch_transform_options(self) -> QWidget:
        """Fetch widget with transform tool options."""
        for q_obj in Krita.get_active_qwindow().findChildren(QWidget):
            if q_obj.objectName() == "KisToolTransform option widget":
                return q_obj  # type: ignore
        raise RuntimeError("Transform options not found.")

    def _fetch_mode_button(self, mode: TransformMode) -> QToolButton:
        """Fetch a button that activates a given mode."""
        for q_obj in self._transform_options.findChildren(QToolButton):
            if q_obj.objectName() == mode.button_name:
                return q_obj  # type: ignore
        raise RuntimeError(f"Could not find the {mode.name} button.")

    def _fetch_apply_button(self) -> QPushButton:
        """Fetch a button that applies the transformation."""
        buttons = self._transform_options.findChildren(QPushButton)
        if not buttons:
            raise RuntimeError("Could not find the apply button.")
        return max(buttons, key=lambda button: button.x())  # type: ignore
