"""Central file which defines extension class and adds it to krita."""

from .shortcut_library.plugin_actions.krita_api_wrapper import (
    Krita,
    Extension
)
from .shortcut_library import ReleaseKeyEventFilter, ActionManager
from .actions import actions


class ToolModifiers(Extension):
    """Krita extension that adds complex keyboard shortcuts."""

    def __init__(self, parent):
        """Initialize extension, create single event filter."""
        super(ToolModifiers, self).__init__(parent)
        self.event_filter = ReleaseKeyEventFilter()

    def setup(self):
        """Obligatory override of abstract class."""
        pass

    def createActions(self, window):
        """Initialize manager of actions which binds them to event filter."""
        manager = ActionManager(window, self.event_filter)
        for action in actions:
            manager.bind_action(action)


# Add extension to krita
Krita.add_extension(ToolModifiers)
