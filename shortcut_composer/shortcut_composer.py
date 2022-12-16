"""Main file which defines extension class and adds it to krita."""

from PyQt5.QtWidgets import QWidgetAction

from api_krita import Krita, Extension  # type: ignore
from input_adapter import ActionManager
from .actions import create_actions
from .composer_utils import SettingsDialog, TransformModeActions


class ShortcutComposer(Extension):
    """Krita extension that adds complex keyboard shortcuts."""

    _pie_settings_dialog: SettingsDialog
    _settings_action: QWidgetAction
    _reload_action: QWidgetAction
    _manager: ActionManager

    def setup(self) -> None:
        """Obligatory override of abstract class method."""

    def createActions(self, window) -> None:
        """Create ActionManager which holds and binds them to krita."""
        self._transform_modes = TransformModeActions()
        self._transform_modes.create_actions(window)

        self._pie_settings_dialog = SettingsDialog()
        self._settings_action = Krita.create_action(
            window=window,
            name="Shortcut Composer Settings",
            group="tools/scripts",
            callback=self._pie_settings_dialog.show)
        self._reload_action = Krita.create_action(
            window=window,
            name="Reload Shortcut Composer",
            callback=self.reload_composer)

        self._manager = ActionManager(window)
        self.reload_composer()

    def reload_composer(self):
        for action in create_actions():
            self._manager.bind_action(action)
