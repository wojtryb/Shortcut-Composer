# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from PyQt5.QtWidgets import QWidgetAction

from krita import Extension
from api_krita import Krita
from api_krita.actions import TransformModeActions
from actions import create_actions
from composer_utils import SettingsDialog
from input_adapter import ActionManager


@dataclass
class GarbageProtector:
    """Stores plugin objects, to protect them from garbage collector."""

    transform_modes: TransformModeActions
    """Creates and stores actions for transform modes."""
    settings_dialog: SettingsDialog
    """QDialog with plugin settings."""
    settings_action: QWidgetAction
    """Displays the settings dialog."""
    action_manager: ActionManager
    """Binds complex actions to krita and holds them."""
    reload_action: QWidgetAction
    """Reloads complex action implementations."""

    def is_alive(self) -> bool:
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
        self._protectors: list[GarbageProtector] = []
        Krita.add_theme_change_callback(self._reload_composer)

    def setup(self) -> None: """Obligatory abstract method override."""

    def createActions(self, window) -> None:
        """Create window components. Called by krita for each new window."""
        self._protectors.append(GarbageProtector(
            transform_modes=TransformModeActions(window),
            settings_dialog=(settings := SettingsDialog()),
            settings_action=self._create_settings_action(window, settings),
            action_manager=ActionManager(window),
            reload_action=self._create_reload_action(window)))

        self._reload_composer()

    def _reload_composer(self) -> None:
        """Reload all core actions for every window."""
        for protector in reversed(self._protectors):
            if not protector.is_alive():
                self._protectors.remove(protector)

        for protector in self._protectors:
            for action in create_actions():
                protector.action_manager.bind_action(action)

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

    def _create_reload_action(self, window) -> QWidgetAction:
        """Create krita action, which reloads all core actions."""
        return Krita.create_action(
            window=window,
            name="Reload Shortcut Composer",
            callback=self._reload_composer)
