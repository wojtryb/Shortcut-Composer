from typing import Protocol
from PyQt5.QtWidgets import QWidgetAction

from .settings_dialog import SettingsDialog


class SettingsHandler:
    """
    Creates and stores `ActionContainers` from `PluginActions`.

    `QWidgetAction` and `ShortcutAdapter` are created and stored in
    container along with passed `PluginAction` by using the
    bind_action() method.
    """

    class Window(Protocol):
        def createAction(
            self,
            name: str,
            description: str,
            menu: str, /
        ) -> QWidgetAction: ...

    def __init__(self, window: Window):
        self._window = window
        self._dialog = SettingsDialog()

    def create_settings(self):
        self.settings_action = self._window.createAction(
            "Shortcut Composer Settings",
            "Shortcut Composer Settings",
            "tools/scripts")
        self.settings_action.setAutoRepeat(False)
        self.settings_action.triggered.connect(self._dialog.show)
