from dataclasses import dataclass
from typing import List

from PyQt5.QtWidgets import QWidgetAction

from .plugin_actions._interfaces import PluginAction
from .event_filter import ReleaseKeyEventFilter
from ._shortcut import Shortcut


@dataclass
class ActionContainer:

    action: PluginAction
    krita_action: QWidgetAction
    shortcut: Shortcut

    def __post_init__(self):
        self.krita_action.setAutoRepeat(False)
        self.krita_action.triggered.connect(self.shortcut.on_key_press)


class ActionManager:

    def __init__(self, window, event_filter: ReleaseKeyEventFilter):
        self._window = window
        self._event_filter = event_filter
        self._stored_actions: List[ActionContainer] = []

    def bind_action(self, action: PluginAction) -> ActionContainer:
        krita_action: QWidgetAction = self._window.createAction(
            action.action_name,
            action.action_name,
            ""
        )
        shortcut = Shortcut(action)
        self._event_filter.register_release_callback(
            shortcut.event_filter_callback)

        container = ActionContainer(action, krita_action, shortcut)
        self._stored_actions.append(container)

        return container
