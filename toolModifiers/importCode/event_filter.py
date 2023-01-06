from typing import Callable

from krita import QMdiArea
from PyQt5.QtCore import QEvent


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
