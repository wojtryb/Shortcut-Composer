from threading import Thread, Lock
from time import sleep
from typing import Literal, List

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
                 instructions: List[Instruction] = [],
                 sign: Literal[1, -1] = 1,
                 time_interval=0.3) -> None:
        super().__init__(
            name=name,
            time_interval=time_interval,
            instructions=instructions)

        self._handler = handler
        self._sign = sign
        self._lock = Lock()

    def on_key_press(self) -> None:
        """Start tracking with handler."""
        self._lock.acquire()
        super().on_key_press()
        cursor = Krita.get_cursor()
        return self._handler.start(lambda: self._sign*cursor.y())

    def on_every_key_release(self) -> None:
        """End tracking with handler."""
        super().on_every_key_release()
        self._handler.stop()
        self._lock.release()


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
                 sign: Literal[1, -1] = 1,
                 time_interval=0.3) -> None:
        super().__init__(
            name=name,
            time_interval=time_interval,
            instructions=instructions)

        self._horizontal_handler = horizontal_handler
        self._vertical_handler = vertical_handler
        self._sign = sign
        self._lock = Lock()

    def on_key_press(self) -> None:
        """Start a thread which decides which handler to start."""
        Thread(target=self._pick_slider, daemon=True).start()

    def _pick_slider(self) -> None:
        """Wait for inital movement to activate the right handler."""
        self._lock.acquire()
        super().on_key_press()
        cursor = Krita.get_cursor()
        start_point = (cursor.x(), cursor.y())
        while True:
            delta_hor = abs(start_point[0] - cursor.x())
            delta_ver = abs(start_point[1] - cursor.y())
            if abs(delta_hor - delta_ver) >= 10:
                break
            sleep(0.05)

        if delta_hor > delta_ver:
            self._horizontal_handler.start(cursor.x)
        else:
            self._vertical_handler.start(lambda: -cursor.y())

    def on_every_key_release(self) -> None:
        """End tracking with handler, regardless of which one was started."""
        super().on_every_key_release()
        self._horizontal_handler.stop()
        self._vertical_handler.stop()
        self._lock.release()
