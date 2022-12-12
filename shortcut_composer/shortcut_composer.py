"""Main file which defines extension class and adds it to krita."""

from api_krita import Extension  # type: ignore
from input_adapter import ActionManager
from .actions import actions
from .templates.pie_menu_utils import SettingsHandler


class ShortcutComposer(Extension):
    """Krita extension that adds complex keyboard shortcuts."""

    _manager: ActionManager

    def setup(self) -> None:
        """Obligatory override of abstract class method."""

    def createActions(self, window) -> None:
        """Create ActionManager which holds and binds them to krita."""
        self._settings = SettingsHandler(window)
        self._manager = ActionManager(window)
        for action in actions:
            self._manager.bind_action(action)
