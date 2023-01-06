"""Main file which defines extension class and adds it to krita."""

from api_krita import Krita, Extension  # type: ignore
from input_adapter import ActionManager
from .actions import actions


class ShortcutComposer(Extension):
    """Krita extension that adds complex keyboard shortcuts."""

    manager: ActionManager

    def setup(self) -> None:
        """Obligatory override of abstract class."""

    def createActions(self, window) -> None:
        """Initialize manager of actions which binds them to krita."""
        self.manager = ActionManager(window)
        for action in actions:
            self.manager.bind_action(action)


# Add extension to krita
Krita.add_extension(ShortcutComposer)
