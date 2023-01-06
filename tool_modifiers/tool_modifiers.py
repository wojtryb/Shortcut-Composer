from krita import Krita, Extension

from .importCode import ReleaseKeyEventFilter, ActionCreator
from .importCode.plugin_actions import (
    TemporaryTool,
    TemporaryEraser,
    TemporaryAlphaLock,
    CyclicTool)

from .config import cyclic_tools, temporary_tools


class ToolModifiers(Extension):

    def __init__(self, parent):
        super(ToolModifiers, self).__init__(parent)
        self.actions = []
        self.event_filter = ReleaseKeyEventFilter()

    def setup(self):
        pass

    def createActions(self, window):
        creator = ActionCreator(window, self.event_filter)

        for action_name, krita_tool in temporary_tools.items():
            self.actions.append(creator.create_action(
                TemporaryTool(action_name, krita_tool))
            )

        for action_name, tools_to_cycle in cyclic_tools.items():
            self.actions.append(creator.create_action(
                CyclicTool(action_name, tools_to_cycle))
            )

        self.actions.append(creator.create_action(TemporaryEraser()))
        self.actions.append(creator.create_action(TemporaryAlphaLock()))


Krita.instance().addExtension(ToolModifiers(Krita.instance()))
