from typing import Any, List, Union

from .controllers import Controller
from .helpers import Range
from .interpreters import create_interpreter


class EmptyHandler:

    def set_start_value(self, mouse: int):
        pass

    def update(self, mouse: int):
        pass


class Handler(EmptyHandler):
    def __init__(
        self,
        controller: Controller,
        values_to_cycle: Union[List[Any], Range],
        default_value: Any,
        sensitivity: int = 50
    ):
        self.__controller = controller
        self.__values_to_cycle = values_to_cycle
        self.__default_value = self.__values_to_cycle.index(default_value)
        self.interpreter = create_interpreter(values_to_cycle, sensitivity)

    def set_start_value(self, mouse: int):
        self.last_mouse = mouse
        try:
            current_value = self.__values_to_cycle.index(
                self.__controller.get_value())
        except ValueError:
            current_value = self.__default_value
        self.interpreter.calibrate(mouse, current_value)

    def update(self, mouse: int):
        self.last_mouse = mouse
        value_to_set = self.interpreter.at(mouse)
        self.__controller.set_value(value_to_set)

    def delta(self):
        return self.interpreter.start_mouse - self.last_mouse
