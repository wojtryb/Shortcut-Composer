from threading import Thread
from time import sleep
from typing import Any, Callable

from data_components import Slider
from .mouse_interpreter import MouseInterpreter
from .slider_values import create_slider_values


class SliderHandler:
    def __init__(self, slider: Slider):
        self.__slider = slider
        self.to_cycle = create_slider_values(self.__slider.values)
        self.__working = False

        self.__interpreter: MouseInterpreter

    def start(self, mouse_getter: Callable[[], int]) -> None:
        self.__working = True
        self.__slider.controller.refresh()
        self.__interpreter = MouseInterpreter(
            min=self.to_cycle.min,
            max=self.to_cycle.max,
            mouse_origin=mouse_getter(),
            start_value=self.__get_current_value(),
            sensitivity=self.__slider.sensitivity,
        )
        Thread(target=self._loop, args=[mouse_getter], daemon=True).start()

    def stop(self):
        self.__working = False

    def _loop(self, mouse_getter: Callable[[], int]) -> None:
        while self.__working:
            self._handle(mouse_getter())
            sleep(0.05)

    def _handle(self, mouse: int) -> None:
        clipped_value = self.__interpreter.mouse_to_value(mouse)
        to_set = self.to_cycle.at(clipped_value)
        self.__slider.controller.set_value(to_set)

    def __get_current_value(self) -> Any:
        try:
            return self.to_cycle.index(self.__slider.controller.get_value())
        except ValueError:
            return self.to_cycle.default_value
