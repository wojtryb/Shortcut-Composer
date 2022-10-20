from .shortcut_library.plugin_actions.krita_api_wrapper import (
    Krita,
    Extension
)
from .shortcut_library import ReleaseKeyEventFilter, ActionManager
from .config import actions


class ToolModifiers(Extension):

    def __init__(self, parent):
        super(ToolModifiers, self).__init__(parent)
        self.actions = []
        self.event_filter = ReleaseKeyEventFilter()

    def setup(self):
        pass

    def createActions(self, window):
        creator = ActionManager(window, self.event_filter)
        for action in actions:
            creator.bind_action(action)


Krita.add_extension(ToolModifiers)
