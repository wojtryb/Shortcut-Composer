from typing import Callable

from PyQt5.QtCore import QEvent
from .plugin_actions.krita_api_wrapper import QMdiArea


class ReleaseKeyEventFilter(QMdiArea):

    def __init__(self):
        super().__init__(None)
        self._release_callbacks = []

    def register_release_callback(self, callback: Callable[[QEvent], None]):
        self._release_callbacks.append(callback)

    def eventFilter(self, _, event):
        if event.type() == QEvent.KeyRelease:
            for callback in self._release_callbacks:
                callback(event)

        return False
