from dataclasses import dataclass
from typing import Any, List, Union

from ...krita_api.controllers import Controller
from .mouse_interpreter import MouseInterpreter
from .slider_values import create_slider_values, Range


class Slider:

    @dataclass
    class MouseTracker:
        start: float = .0
        last: float = .0

        @property
        def delta(self):
            return self.start - self.last

    def __init__(
        self,
        controller: Controller,
        values_to_cycle: Union[List[Any], Range],
        default_value: Any,
        sensitivity: int = 50
    ):
        self.__controller = controller
        self.__to_cycle = create_slider_values(values_to_cycle, default_value)
        self.interpreter = MouseInterpreter(self.__to_cycle, sensitivity)
        self.mouse = self.MouseTracker()

    def set_start_value(self, mouse: int):
        self.mouse.start = mouse
        self.mouse.last = mouse

        value = self.__get_current_value()
        self.interpreter.calibrate(mouse, value)

    def handle(self, mouse: int):
        self.mouse.last = mouse

        clipped_value = self.interpreter.mouse_to_value(mouse)
        to_set = self.__to_cycle.at(clipped_value)
        self.__controller.set_value(to_set)

    def __get_current_value(self):
        try:
            return self.__to_cycle.index(self.__controller.get_value())
        except ValueError:
            return self.__to_cycle.default_value

    def _change_values(self, values: List[Any]):
        self.__to_cycle.values_to_cycle = values
        self.__to_cycle.max = len(values) - 0.51


class EmptySlider(Slider):

    def __init__(self): ...
    def set_start_value(self, mouse: int): ...
    def handle(self, mouse: int): ...
