from krita import Krita, Extension

from .shortcut_library import ReleaseKeyEventFilter, ActionManager
from .shortcut_library.plugin_actions import (
    TemporaryTool,
    TemporaryEraser,
    TemporaryAlphaLock,
    CyclicTool,
    CyclicPreset,
)

from .config import cyclic_tools, temporary_tools


class ToolModifiers(Extension):

    def __init__(self, parent):
        super(ToolModifiers, self).__init__(parent)
        self.actions = []
        self.event_filter = ReleaseKeyEventFilter()

    def setup(self):
        pass

    def createActions(self, window):
        creator = ActionManager(window, self.event_filter)

        for action_name, krita_tool in temporary_tools.items():
            creator.bind_action(TemporaryTool(action_name, krita_tool))

        for action_name, tools_to_cycle in cyclic_tools.items():
            creator.bind_action(CyclicTool(action_name, tools_to_cycle))

        creator.bind_action(TemporaryEraser())
        creator.bind_action(TemporaryAlphaLock())
        creator.bind_action(CyclicPreset(
            action_name="Preset (cycle)",
            _values_to_cycle=[
                "wojtryb6 R 02a square DA impasto",
                "wojtryb6 R 02b square DA impasto pat",
                "wojtryb6 R 03 square strong impasto",
                "wojtryb6 R 04 square twoSided impasto",
                "wojtryb6 R 05 watercolor",
            ],
            _default_value="wojtryb6 R 01 horizontal DA"
        ))


Krita.instance().addExtension(ToolModifiers(Krita.instance()))