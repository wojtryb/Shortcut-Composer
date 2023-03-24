# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

__version__ = "1.1.1"
__author__ = "Wojciech Trybus"

from typing import List
from dataclasses import dataclass
from PyQt5.QtWidgets import QWidgetAction, QWidget

from api_krita import Krita, Extension  # type: ignore
from api_krita.actions import TransformModeActions
from actions import create_actions
from composer_utils import SettingsDialog
from input_adapter import ActionManager


@dataclass
class GarbageProtector:
    """
    Stores plugin objects, to protect them from garbage collector.

    - TransformModeActions which create and store actions for transform modes
    - QDialog with plugin settings,
    - Action for displaying the settings dialog above
    - Manager for complex actions which which holds and binds them to krita
    - Action for reloading the complex action implementations
    """
    transform_modes: TransformModeActions
    settings_dialog: SettingsDialog
    settings_action: QWidgetAction
    action_manager: ActionManager
    reload_action: QWidgetAction

    def is_alive(self):
        """Return False if the action was deleted by C++"""
        try:
            self.settings_action.isEnabled()
        except RuntimeError:
            return False
        return True


class ShortcutComposer(Extension):
    """Krita extension that adds complex actions invoked with keyboard."""

    def __init__(self, parent) -> None:
        """Add callback to reload actions on theme change."""
        super().__init__(parent)
        self._protectors: List[GarbageProtector] = []
        Krita.add_theme_change_callback(self._reload_composer)

    def setup(self) -> None: """Obligatory abstract method override."""

    def createActions(self, window) -> None:
        """Create window components. Called by krita for each new window."""
        self._protectors.append(GarbageProtector(
            transform_modes=TransformModeActions(window),
            # settings_dialog=(settings := SettingsDialog()),
            # settings_action=self._create_settings_action(window, settings),
            settings_dialog=QWidget(),
            settings_action=QWidget(),
            action_manager=ActionManager(window),
            reload_action=self._create_reload_action(window)))

        self._reload_composer()

    def _create_reload_action(self, window) -> QWidgetAction:
        """Create krita action which reloads all core actions."""
        return Krita.create_action(
            window=window,
            name="Reload Shortcut Composer",
            group="tools/scripts",
            callback=self._reload_composer)

    def _create_settings_action(
        self,
        window,
        settings_dialog: SettingsDialog
    ) -> QWidgetAction:
        """Create krita action which opens the extension settings dialog."""
        return Krita.create_action(
            window=window,
            name="Configure Shortcut Composer",
            group="tools/scripts",
            callback=settings_dialog.show)

    def _reload_composer(self) -> None:
        """Reload all core actions for every window."""
        for protector in reversed(self._protectors):
            if not protector.is_alive():
                self._protectors.remove(protector)

        for protector in self._protectors:
            for action in create_actions():
                protector.action_manager.bind_action(action)
