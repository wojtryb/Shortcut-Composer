from dataclasses import dataclass

from .event_filter import ReleaseKeyEventFilter
from .shortcut import ActionElements, Shortcut


@dataclass
class Action:
    action_name: str
    krita_action: None
    shortcut: Shortcut

    def __post_init__(self):
        self.krita_action.setAutoRepeat(False)
        self.krita_action.triggered.connect(self.shortcut.on_key_press)


class ActionCreator:
    def __init__(self, window, event_filter: ReleaseKeyEventFilter):
        self.window = window
        self.event_filter = event_filter

    def create_action(
        self,
        human_name,
        set_low_function,
        set_high_function,
        is_high_state_function
    ) -> Action:
        'creates a single shortcut action'
        krita_action = self.window.createAction(human_name, human_name, "")

        shortcut = Shortcut(ActionElements(
            human_name,
            set_low_function,
            set_high_function,
            is_high_state_function,
        ))
        self.event_filter.register_release_callback(
            shortcut.event_filter_callback)

        return Action(human_name, krita_action, shortcut)
