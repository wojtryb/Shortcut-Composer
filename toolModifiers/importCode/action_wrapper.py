from dataclasses import dataclass

from .key_filter import ActionElements, KeyFilter
from .shortcut import Shortcut


@dataclass
class ActionWrapper:
    action_name: str
    krita_action: None
    shortcut: Shortcut


class ActionCreator:
    def __init__(self, window) -> None:
        self.window = window

    def create_shortcut(
        self,
        human_name,
        set_low_function,
        set_high_function,
        is_high_state_function
    ) -> ActionWrapper:
        'creates a single shortcut action'
        action = self.window.createAction(human_name, human_name, "")
        action.setAutoRepeat(False)
        shortcut = Shortcut(ActionElements(
            human_name,
            set_low_function,
            set_high_function,
            is_high_state_function,
        ))

        action.triggered.connect(shortcut.on_key_press)

        return ActionWrapper(
            human_name,
            action,
            shortcut
        )
