from dataclasses import dataclass
from .keyFilter import ActionElements, KeyFilter


@dataclass
class ActionWrapper:
    action_name: str
    action_description: str
    krita_action: None
    krita_filter: None


class ActionCreator:
    def __init__(self, window) -> None:
        self.window = window

    def create_shortcut(
        self,
        human_name,
        krita_name,
        set_low_function,
        set_high_function,
        is_high_state_function
    ):
        'creates a single shortcut action'
        action = self.window.createAction(human_name, human_name, "")
        action.setAutoRepeat(False)
        action_filter = KeyFilter(ActionElements(
            human_name,
            krita_name,
            set_low_function,
            set_high_function,
            is_high_state_function,
        ))

        self.window.qwindow().installEventFilter(action_filter)
        action.triggered.connect(action_filter.keyPress)

        # return action_filter
        return ActionWrapper(
            krita_name,
            human_name,
            action,
            action_filter
        )
