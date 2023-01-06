from dataclasses import dataclass
from threading import Thread, Lock
from time import sleep
from typing import Literal

from api_krita import Krita
from input_adapter import PluginAction
from core_components import InstructionHolder
from .slider_handler import SliderHandler


@dataclass
class SingleAxisTracker(PluginAction):
    """
    Track the mouse along one axis to switch values.

    Tracking is performed as long as the key is pressed.
    This class only grants the PluginAction interface, while the main
    logic is located in passed SliderHandler.
    """

    name: str
    handler: SliderHandler
    instructions: InstructionHolder
    sign: Literal[1, -1] = 1

    _time_interval = 0
    _lock = Lock()

    def on_key_press(self) -> None:
        """Start tracking with handler."""
        self._lock.acquire()
        self.instructions.enter()
        cursor = Krita.get_cursor()
        return self.handler.start(lambda: self.sign*cursor.y())

    def on_every_key_release(self) -> None:
        """End tracking with handler."""
        self.handler.stop()
        self.instructions.exit()
        self._lock.release()


@dataclass
class DoubleAxisTracker(PluginAction):
    """
    Track the mouse along the axis which had the biggest initial movement.

    Tracking is performed as long as the key is pressed.
    This class only grants the PluginAction interface, while the main
    logic is located in passed SliderHandler.
    """

    name: str
    horizontal_handler: SliderHandler
    vertical_handler: SliderHandler
    instructions: InstructionHolder

    _time_interval = 0
    _lock = Lock()

    def on_key_press(self) -> None:
        """Start a thread which decides which handler to start."""
        Thread(target=self._pick_slider, daemon=True).start()

    def _pick_slider(self) -> None:
        """Wait for inital movement to activate the right handler."""
        self._lock.acquire()
        self.instructions.enter()
        cursor = Krita.get_cursor()
        start_point = (cursor.x(), cursor.y())
        while True:
            delta_hor = abs(start_point[0] - cursor.x())
            delta_ver = abs(start_point[1] - cursor.y())
            if abs(delta_hor - delta_ver) >= 10:
                break
            sleep(0.05)

        if delta_hor > delta_ver:
            self.horizontal_handler.start(cursor.x)
        else:
            self.vertical_handler.start(lambda: -cursor.y())

    def on_every_key_release(self) -> None:
        """End tracking with handler, regardless of which one was started."""
        self.horizontal_handler.stop()
        self.vertical_handler.stop()
        self.instructions.exit()
        self._lock.release()
