from typing import Callable, List, TypeVar
T = TypeVar("T")


class NotifyingList(List[T]):
    def __init__(self, *args, **kwargs):
        self._callbacks = []
        super().__init__(*args, **kwargs)

    def register_callback(self, callback: Callable[[], None]):
        self._callbacks.append(callback)

    def notify_about_change(self):
        for callback in self._callbacks:
            callback()
