from time import time

from PyQt5.QtGui import QKeyEvent

from .plugin_actions.krita_api_wrapper import Krita
from .plugin_actions.interfaces import PluginAction


class Shortcut:
    """
    Maps krita key events to custom ones from PluginAction.

    Krita events:
    - on_key_press (recognised when krita action is triggered)
    - on_key_release (found by event filter)

    Custom action events:
    - on_key_press
    - on_short_key_release (release directly after the press)
    - on_long_key_release (release long time after the press)
    - on_every_key_release (called after short or long release callback)
    """

    def __init__(self, action: PluginAction):
        """Store action which will be steered, and time counting objects."""
        self.action = action
        self.key_released = True
        self.last_press_time = time()

    def on_key_press(self):
        """Callback to run when krita action is triggered."""
        self.key_released = False
        self.last_press_time = time()
        self.action.on_key_press()

    def _on_key_release(self):
        """Run when key event is recognised as release of related key."""
        self.key_released = True
        if time() - self.last_press_time < self.action.time_interval:
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
