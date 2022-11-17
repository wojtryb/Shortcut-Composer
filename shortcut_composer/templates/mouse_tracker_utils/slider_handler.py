from threading import Thread
from time import sleep
from typing import Callable, Iterable

from data_components import Slider, Range
from .new_types import MouseInput, Interpreted
from .mouse_interpreter import MouseInterpreter
from .slider_values import (
    RangeSliderValues,
    ListSliderValues,
    SliderValues,
)


class SliderHandler:

    MouseGetter = Callable[[], MouseInput]

    def __init__(self, slider: Slider):
        self.__slider = slider
        self.__to_cycle = self.__create_slider_values()
        self.__working = False

        self.__interpreter: MouseInterpreter

    def start(self, mouse_getter: MouseGetter) -> None:
        self.__working = True
        self.__slider.controller.refresh()
        Thread(target=self._loop, args=[mouse_getter], daemon=True).start()

    def stop(self):
        self.__working = False

    def _loop(self, mouse_getter: MouseGetter) -> None:
        self._block_until_deadzone(mouse_getter)
        self.__interpreter = MouseInterpreter(
            min=self.__to_cycle.min,
            max=self.__to_cycle.max,
            mouse_origin=mouse_getter(),
            start_value=self.__get_current_value(),
            pixels_in_unit=self.__slider.pixels_in_unit,
        )
        while self.__working:
            self._handle(mouse_getter())
            sleep(0.05)

    def _block_until_deadzone(self, mouse_getter: MouseGetter) -> None:
        start_point = mouse_getter()
        while abs(start_point - mouse_getter()) <= self.__slider.deadzone:
            if not self.__working:
                return
            sleep(0.05)

    def _handle(self, mouse: MouseInput) -> None:
        clipped_value = self.__interpreter.interpret(mouse)
        to_set = self.__to_cycle.at(clipped_value)
        self.__slider.controller.set_value(to_set)

    def __create_slider_values(self) -> SliderValues:
        """Return the right values adapter based on passed data type."""
        values = self.__slider.values

        if isinstance(values, Iterable):
            return ListSliderValues(values)
        elif isinstance(values, Range):
            return RangeSliderValues(values)

        raise RuntimeError(f"Wrong type: {values}")

    def __get_current_value(self) -> Interpreted:
        return self.__to_cycle.index(self.__slider.controller.get_value())
