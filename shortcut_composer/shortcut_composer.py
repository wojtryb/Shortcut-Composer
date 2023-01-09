# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QWidgetAction

from api_krita import Krita, Extension  # type: ignore
from api_krita.actions import TransformModeActions
from actions import create_actions
from composer_utils import SettingsDialog
from input_adapter import ActionManager


class ShortcutComposer(Extension):
    """Krita extension that adds complex actions invoked with keyboard."""

    _pie_settings_dialog: SettingsDialog
    _settings_action: QWidgetAction
    _reload_action: QWidgetAction
    _manager: ActionManager

    def setup(self) -> None: """Obligatory abstract method override."""

    def createActions(self, window) -> None:
        """
        Start the extension. Called by krita during plugin init phase.

        - Create usual actions for transform modes using `TransformModeActions`
        - Create usual actions for reloading the extension and settings dialog
        - Add a callback to reload plugin when krita theme changes
        - Create complex action manager which holds and binds them to krita
        """
        self._transform_modes = TransformModeActions(window)

        self._pie_settings_dialog = SettingsDialog()
        self._reload_action = self._create_reload_action(window)
        self._settings_action = self._create_settings_action(window)

        Krita.add_theme_change_callback(self._reload_composer)

        self._manager = ActionManager(window)
        self._reload_composer()

    def _create_reload_action(self, window) -> QWidgetAction:
        """Create krita action which reloads all core actions."""
        return Krita.create_action(
            window=window,
            name="Reload Shortcut Composer",
            group="tools/scripts",
            callback=self._reload_composer)

    def _create_settings_action(self, window) -> QWidgetAction:
        """Create krita action which opens the extension settings dialog."""
        return Krita.create_action(
            window=window,
            name="Configure Shortcut Composer",
            group="tools/scripts",
            callback=self._pie_settings_dialog.show)

    def _reload_composer(self) -> None:
        """Reload all core actions."""
        for action in create_actions():
            self._manager.bind_action(action)
