from threading import Thread, Lock
from time import sleep
from typing import List

from api_krita import Krita
from input_adapter import PluginAction
from core_components import Instruction
from data_components import Slider
from .slider_handler import SliderHandler
from .new_types import MouseInput


def pick_mouse_getter(is_horizontal: bool):
    cursor = Krita.get_cursor()
    if is_horizontal:
        return lambda: MouseInput(cursor.x())
    return lambda: MouseInput(-cursor.y())


class SingleAxisTracker(PluginAction):
    """
    Track the mouse along one axis to switch values.

    Tracking is performed as long as the key is pressed.
    This class only grants the PluginAction interface, while the main
    logic is located in passed SliderHandler.
    """

    def __init__(self, *,
                 name: str,
                 slider: Slider,
                 is_horizontal: bool,
                 instructions: List[Instruction] = [],
                 time_interval: float = 0.3) -> None:
        super().__init__(
            name=name,
            time_interval=time_interval,
            instructions=instructions)

        self._is_horizontal = is_horizontal
        self._handler = SliderHandler(slider)

    def on_key_press(self) -> None:
        """Start tracking with handler."""
        super().on_key_press()
        self._handler.start(pick_mouse_getter(self._is_horizontal))

    def on_every_key_release(self) -> None:
        """End tracking with handler."""
        super().on_every_key_release()
        self._handler.stop()


class DoubleAxisTracker(PluginAction):
    """
    Track the mouse along the axis which had the biggest initial movement.

    Tracking is performed as long as the key is pressed.
    This class only grants the PluginAction interface, while the main
    logic is located in SliderHandler which uses passed Slider.
    """

    def __init__(self, *,
                 name: str,
                 horizontal_slider: Slider,
                 vertical_slider: Slider,
                 instructions: List[Instruction] = [],
                 time_interval: float = 0.3) -> None:
        super().__init__(
            name=name,
            time_interval=time_interval,
            instructions=instructions)

        self._horizontal_handler = SliderHandler(horizontal_slider)
        self._vertical_handler = SliderHandler(vertical_slider)
        self._lock = Lock()
        self._is_working = False

    def on_key_press(self) -> None:
        """Start a thread which decides which handler to start."""
        super().on_key_press()
        Thread(target=self._start_after_picking_slider, daemon=True).start()

    def _start_after_picking_slider(self) -> None:
        """Wait for inital movement to activate the right handler."""
        comparator = self.MouseComparator()
        with self._lock:
            self._is_working = True
            while comparator.delta_x <= 10 and comparator.delta_y <= 10:
                if not self._is_working:
                    return
                sleep(0.05)

            mouse_getter = pick_mouse_getter(comparator.is_horizontal)
            if comparator.is_horizontal:
                self._horizontal_handler.start(mouse_getter)
            else:
                self._vertical_handler.start(mouse_getter)

    def on_every_key_release(self) -> None:
        """End tracking with handler, regardless of which one was started."""
        super().on_every_key_release()
        self._is_working = False
        with self._lock:
            self._horizontal_handler.stop()
            self._vertical_handler.stop()

    class MouseComparator:
        def __init__(self) -> None:
            self.cursor = Krita.get_cursor()
            self.start_x = self.cursor.x()
            self.start_y = self.cursor.y()

        @property
        def delta_x(self): return abs(self.start_x - self.cursor.x())
        @property
        def delta_y(self): return abs(self.start_y - self.cursor.y())
        @property
        def is_horizontal(self) -> bool: return self.delta_x > self.delta_y
