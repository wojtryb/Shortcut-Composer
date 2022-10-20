from dataclasses import dataclass
from typing import Any, List, Union

from ..plugin_actions.controllers import Controller
from ..convenience_utils.helpers import Range
from .interpreters import Interpreter
from .value_proxy import create_proxy


class EmptyHandler:

    def delta(self):
        """TODO: not really working"""
        return 0

    def set_start_value(self, mouse: int):
        pass

    def handle(self, mouse: int):
        pass


@dataclass
class MouseTracker:
    start: float = .0
    last: float = .0

    @property
    def delta(self):
        return self.start - self.last


class Handler(EmptyHandler):
    def __init__(
        self,
        controller: Controller,
        values_to_cycle: Union[List[Any], Range],
        default_value: Any,
        sensitivity: int = 50
    ):
        self.__controller = controller
        self.__to_cycle = create_proxy(values_to_cycle, default_value)
        self.interpreter = Interpreter(self.__to_cycle, sensitivity)
        self.mouse = MouseTracker()

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
