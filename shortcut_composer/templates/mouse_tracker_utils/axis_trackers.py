from threading import Thread, Lock
from time import sleep
from typing import List

from api_krita import Krita
from input_adapter import PluginAction
from core_components import Instruction
from .slider_handler import SliderHandler


class SingleAxisTracker(PluginAction):
    """
    Track the mouse along one axis to switch values.

    Tracking is performed as long as the key is pressed.
    This class only grants the PluginAction interface, while the main
    logic is located in passed SliderHandler.
    """

    def __init__(self, *,
                 name: str,
                 handler: SliderHandler,
                 is_horizontal: bool,
                 instructions: List[Instruction] = [],
                 time_interval: float = 0.3) -> None:
        super().__init__(
            name=name,
            time_interval=time_interval,
            instructions=instructions)

        self._is_horizontal = is_horizontal
        self._handler = handler

    def on_key_press(self) -> None:
        """Start tracking with handler."""
        super().on_key_press()
        self._handler.start(self._get_mouse_getter())

    def on_every_key_release(self) -> None:
        """End tracking with handler."""
        super().on_every_key_release()
        self._is_working = False
        self._handler.stop()

    def _get_mouse_getter(self):
        cursor = Krita.get_cursor()

        if self._is_horizontal:
            return cursor.x
        return lambda: -cursor.y()


class DoubleAxisTracker(PluginAction):
    """
    Track the mouse along the axis which had the biggest initial movement.

    Tracking is performed as long as the key is pressed.
    This class only grants the PluginAction interface, while the main
    logic is located in passed SliderHandler.
    """

    def __init__(self, *,
                 name: str,
                 horizontal_handler: SliderHandler,
                 vertical_handler: SliderHandler,
                 instructions: List[Instruction] = [],
                 time_interval: float = 0.3) -> None:
        super().__init__(
            name=name,
            time_interval=time_interval,
            instructions=instructions)

        self._horizontal_handler = horizontal_handler
        self._vertical_handler = vertical_handler
        self._lock = Lock()
        self._is_working = False

    def on_key_press(self) -> None:
        """Start a thread which decides which handler to start."""
        super().on_key_press()
        Thread(target=self._pick_slider, daemon=True).start()

    def _pick_slider(self) -> None:
        """Wait for inital movement to activate the right handler."""
        cursor = Krita.get_cursor()
        start_point = (cursor.x(), cursor.y())
        with self._lock:
            self._is_working = True
            delta_hor = 0
            delta_ver = 0
            while abs(delta_hor - delta_ver) <= 10:
                delta_hor = abs(start_point[0] - cursor.x())
                delta_ver = abs(start_point[1] - cursor.y())
                if not self._is_working:
                    return
                sleep(0.05)

            if delta_hor > delta_ver:
                self._horizontal_handler.start(cursor.x)
            else:
                self._vertical_handler.start(lambda: -cursor.y())

    def on_every_key_release(self) -> None:
        """End tracking with handler, regardless of which one was started."""
        super().on_every_key_release()
        self._is_working = False
        with self._lock:
            self._horizontal_handler.stop()
            self._vertical_handler.stop()
