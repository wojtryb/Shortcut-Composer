"""Main file which defines extension class and adds it to krita."""

from api_krita import Extension  # type: ignore
from input_adapter import ActionManager
from .actions import create_actions
from .composer_utils import SettingsDialog


class ShortcutComposer(Extension):
    """Krita extension that adds complex keyboard shortcuts."""

    _manager: ActionManager

    def setup(self) -> None:
        """Obligatory override of abstract class method."""

    def createActions(self, window) -> None:
        """Create ActionManager which holds and binds them to krita."""
        self._pie_setting_dialog = SettingsDialog()
        self._settings_action = self._create_settings(window)
        self._reload_action = self._create_reload(window)

        self._manager = ActionManager(window)
        self.reload_composer()

    def reload_composer(self):
        for action in create_actions():
            self._manager.bind_action(action)

    def _create_settings(self, window):
        settings_action = window.createAction(
            "Shortcut Composer Settings",
            "Shortcut Composer Settings",
            "tools/scripts")
        settings_action.setAutoRepeat(False)
        settings_action.triggered.connect(self._pie_setting_dialog.show)
        return settings_action

    def _create_reload(self, window):
        reload_action = window.createAction(
            "Reload Shortcut Composer",
            "Reload Shortcut Composer",
            "")
        reload_action.setAutoRepeat(False)
        reload_action.triggered.connect(self.reload_composer)
        return reload_action
