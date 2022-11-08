"""Central file which defines extension class and adds it to krita."""

from api_krita import Krita, Extension
from input_adapter import ActionManager
from .actions import actions


class ShortcutComposer(Extension):
    """Krita extension that adds complex keyboard shortcuts."""

    manager: ActionManager

    def __init__(self, parent):
        """Initialize extension, create single event filter."""
        super(ShortcutComposer, self).__init__(parent)

    def setup(self) -> None:
        """Obligatory override of abstract class."""

    def createActions(self, window) -> None:
        """Initialize manager of actions which binds them to event filter."""
        self.manager = ActionManager(window)
        for action in actions:
            self.manager.bind_action(action)


# Add extension to krita
Krita.add_extension(ShortcutComposer)
