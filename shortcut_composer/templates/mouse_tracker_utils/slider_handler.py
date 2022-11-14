from threading import Thread
from time import sleep
from typing import Callable

from data_components import Slider
from .mouse_interpreter import MouseInterpreter
from .slider_values import create_slider_values
from .new_types import MouseInput, Interpreted

MouseGetter = Callable[[], MouseInput]


class SliderHandler:
    def __init__(self, slider: Slider):
        self.__slider = slider
        self.__to_cycle = create_slider_values(self.__slider.values)
        self.__working = False

        self.__interpreter: MouseInterpreter

    def start(self, mouse_getter: MouseGetter) -> None:
        self.__working = True
        self.__slider.controller.refresh()
        self.__interpreter = MouseInterpreter(
            min=self.__to_cycle.min,
            max=self.__to_cycle.max,
            mouse_origin=mouse_getter(),
            start_value=self.__get_current_value(),
            sensitivity=self.__slider.sensitivity,
        )
        Thread(target=self._loop, args=[mouse_getter], daemon=True).start()

    def stop(self):
        self.__working = False

    def _loop(self, mouse_getter: MouseGetter) -> None:
        while self.__working:
            self._handle(mouse_getter())
            sleep(0.05)

    def _handle(self, mouse: MouseInput) -> None:
        clipped_value = self.__interpreter.interpret(mouse)
        to_set = self.__to_cycle.at(clipped_value)
        self.__slider.controller.set_value(to_set)

    def __get_current_value(self) -> Interpreted:
        try:
            return self.__to_cycle.index(self.__slider.controller.get_value())
        except ValueError:
            return self.__to_cycle.default
