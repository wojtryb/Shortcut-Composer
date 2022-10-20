from dataclasses import dataclass

from PyQt5.QtWidgets import QWidgetAction

from .actions import Action
from .event_filter import ReleaseKeyEventFilter
from .shortcut import Shortcut


@dataclass
class ActionContainer:
    action: Action
    krita_action: QWidgetAction
    shortcut: Shortcut

    def __post_init__(self):
        self.krita_action.setAutoRepeat(False)
        self.krita_action.triggered.connect(self.shortcut.on_key_press)


class ActionCreator:
    def __init__(self, window, event_filter: ReleaseKeyEventFilter):
        self.window = window
        self.event_filter = event_filter

    def create_action(self, action: Action)\
            -> ActionContainer:
        krita_action: QWidgetAction = self.window.createAction(
            action.action_name,
            action.action_name,
            ""
        )
        shortcut = Shortcut(action)
        self.event_filter.register_release_callback(
            shortcut.event_filter_callback)

        return ActionContainer(action, krita_action, shortcut)
