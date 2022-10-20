from krita import Krita

from time import time
from .actions import Action

from ..config import interval


class Shortcut:

    def __init__(self, action: Action):
        self.action = action
        self.key_released = True
        self.last_press_time = time()

    def on_key_press(self):
        'run when user presses a key assigned to this action'
        self.key_released = False
        self.last_press_time = time()

        self.state = self.action.is_high_state()
        if not self.state:
            self.action.set_high()

    def on_key_release(self):
        'run when user released a related key'

        self.key_released = True
        if time() - self.last_press_time > interval or self.state:
            self.action.set_low()

    def _is_event_key_release(self, event):
        return (
            self.tool_shortcut.matches(event.key()) > 0
            and not event.isAutoRepeat()
            and not self.key_released
        )

    def event_filter_callback(self, event):
        if self._is_event_key_release(event):
            self.on_key_release()

    @property
    def tool_shortcut(self):
        return Krita.instance().action(self.action.human_name).shortcut()
