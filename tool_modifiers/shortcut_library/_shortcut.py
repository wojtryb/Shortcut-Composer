from time import time

from PyQt5.QtGui import QKeyEvent

from .plugin_actions.krita_api_wrapper import Krita
from .plugin_actions._interfaces import PluginAction
from ..config import interval


class Shortcut:

    def __init__(self, action: PluginAction):
        self.action = action
        self.key_released = True
        self.last_press_time = time()

    def on_key_press(self):
        'run when user presses a key assigned to this action'
        self.key_released = False
        self.last_press_time = time()
        self.action.on_key_press()

    def _on_key_release(self):
        'run when user released a related key'

        self.key_released = True
        if time() - self.last_press_time < interval:
            self.action.on_short_key_release()
        else:
            self.action.on_long_key_release()
        self.action.on_every_key_release()

    def _is_event_key_release(self, event: QKeyEvent):
        return (
            self.tool_shortcut.matches(event.key()) > 0
            and not event.isAutoRepeat()
            and not self.key_released
        )

    def event_filter_callback(self, event: QKeyEvent):
        if self._is_event_key_release(event):
            self._on_key_release()

    @property
    def tool_shortcut(self):
        return Krita.get_action_shortcut(self.action.action_name)
