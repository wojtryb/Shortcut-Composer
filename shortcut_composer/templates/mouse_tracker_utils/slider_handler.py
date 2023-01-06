from threading import Thread
from time import sleep
from typing import Callable, Iterable

from api_krita import Krita
from data_components import Slider, Range
from .new_types import MouseInput, Interpreted
from .mouse_interpreter import MouseInterpreter
from .slider_values import (
    RangeSliderValues,
    ListSliderValues,
    SliderValues,
)


class SliderHandler:
    """
    When started, tracks the mouse, interprets it and sets corresponding value.

    Arguments:
    - `slider` - configuration dataclass created by the user.
    - `is_horizontal` - allows to track the correct axes.

    On initialization, values to cycle stored in `slider` are wrapped in
    proper `SliderValues` which will provide controller compatibile
    values.

    The handler is running between `start()` and `stop()` calls.

    Right after start, the handler waits for the mouse to move past the
    deadzone which allows to prevent unwanted changes.

    After the deadzone is reached, the value interpreter is created
    using the current mouse position.

    Main handler loop starts:
    - the mouse offset is being interpreted
    - interpreted values allow to fetch controller compatibile values
      from the `SliderValues`
    - `SliderValues` values are being set using the controller.

    Calling stop cancels the process at any step, so that the main loop
    can never be started.
    """

    def __init__(self, slider: Slider, is_horizontal: bool):
        self.__slider = slider
        self.__to_cycle = self.__create_slider_values(slider)
        self.__working = False
        self.__is_horizontal = is_horizontal

        self.__mouse_getter: Callable[[], MouseInput]
        self.__interpreter: MouseInterpreter

    def read_mouse(self) -> MouseInput:
        return self.__mouse_getter()

    def start(self) -> None:
        self.__working = True
        self.__slider.controller.refresh()
        self.__mouse_getter = self.__pick_mouse_getter()
        Thread(target=self._start_after_deadzone, daemon=True).start()

    def stop(self) -> None:
        self.__working = False

    def _start_after_deadzone(self) -> None:
        start_point = self.read_mouse()
        while abs(start_point - self.read_mouse()) <= self.__slider.deadzone:
            if not self.__working:
                return
            sleep(0.05)
        self._value_setting_loop()

    def _value_setting_loop(self) -> None:
        self.__update_interpreter()
        while self.__working:
            clipped_value = self.__interpreter.interpret(self.read_mouse())
            to_set = self.__to_cycle.at(clipped_value)
            self.__slider.controller.set_value(to_set)
            sleep(0.05)

    def __update_interpreter(self):
        self.__interpreter = MouseInterpreter(
            min=self.__to_cycle.min,
            max=self.__to_cycle.max,
            mouse_origin=self.read_mouse(),
            start_value=self.__get_current_interpreted_value(),
            pixels_in_unit=self.__slider.pixels_in_unit,
        )

    def __get_current_interpreted_value(self) -> Interpreted:
        controller_value = self.__slider.controller.get_value()
        return self.__to_cycle.index(controller_value)

    def __pick_mouse_getter(self):
        cursor = Krita.get_cursor()
        if self.__is_horizontal:
            return lambda: MouseInput(cursor.x())
        return lambda: MouseInput(-cursor.y())

    @staticmethod
    def __create_slider_values(slider: Slider) -> SliderValues:
        """Return the right values adapter based on passed data type."""
        if isinstance(slider.values, Iterable):
            return ListSliderValues(slider.values)
        elif isinstance(slider.values, Range):
            return RangeSliderValues(slider.values)

        raise RuntimeError(f"Wrong type: {slider.values}")
