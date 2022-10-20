from krita import Krita, Extension
from .importCode.actions import (
    ToolWrapper,
    EraserWrapper,
    AlphaWrapper,
    CyclicTool)

from .importCode.event_filter import ReleaseKeyEventFilter
from .importCode.action_wrapper import ActionCreator

from .config import tools


class toolModifiers(Extension):
    'the extension'

    def __init__(self, parent):
        super(toolModifiers, self).__init__(parent)
        self.actions = []
        self.event_filter = ReleaseKeyEventFilter()

    def setup(self):
        pass

    def createActions(self, window):
        """
        run on startup - creates all keyboard shortcuts in the plugin - tool
        modifiers needed by the user, and toggles for eraser and preserve alpha
        """
        creator = ActionCreator(window, self.event_filter)

        for human_name, krita_name in tools.items():
            tool = ToolWrapper(krita_name, human_name)
            self.actions.append(creator.create_action(tool))

        self.actions.append(creator.create_action(EraserWrapper()))
        self.actions.append(creator.create_action(AlphaWrapper()))
        self.actions.append(creator.create_action(CyclicTool([
            "KritaShape/KisToolBrush",
            "KisToolSelectOutline",
            "KritaFill/KisToolGradient",
            "KritaShape/KisToolLine",
            "KisToolTransform",
        ])))


Krita.instance().addExtension(toolModifiers(Krita.instance()))
