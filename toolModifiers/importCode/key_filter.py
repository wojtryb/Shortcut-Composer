from time import time
from dataclasses import dataclass
from typing import Callable

from krita import *
from PyQt5.QtCore import QEvent

from ..SETUP import INTERVAL


@dataclass
class ActionElements:
    human_name: str
    set_low_function: Callable[[], None]
    set_high_function: Callable[[], None]
    is_high_state_function: Callable[[], None]


class KeyFilter(QMdiArea):
    """
    object that handles one shortcut, installed on krita window and
    catches all keyboard inputs waiting for the correct one
    """

    def __init__(self, elements: ActionElements) -> None:
        super().__init__(None)
        self.elements = elements
        self.key_released = True
        self.last_press_time = time()

    def handle_key_press(self):
        'run when user presses a key assigned to this action'
        self.key_released = False
        self.last_press_time = time()

        # if the handled action wasnt already active, activate it
        self.state = self.elements.is_high_state_function()
        if not self.state:
            self.elements.set_high_function()

    def handle_key_release(self):
        'run when user released a related key'

        self.key_released = True
        if time() - self.last_press_time > INTERVAL or self.state:
            self.elements.set_low_function()

    def eventFilter(self, obj, e):
        'activated each time user does anything - search for key releases'

        if e.type() != QEvent.KeyRelease:
            return False

        if (
            self.tool_shortcut.matches(e.key()) > 0
            and not e.isAutoRepeat()
            and not self.key_released
        ):
            self.handle_key_release()
        return False

    @property
    def tool_shortcut(self):
        return Krita.instance().action(self.elements.human_name).shortcut()
