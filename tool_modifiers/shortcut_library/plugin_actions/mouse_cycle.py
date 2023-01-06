from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from threading import Thread
from time import sleep
from typing import Any, List, Union

from .krita_api_wrapper import Krita
from .interfaces import PluginAction
from .controllers import Controller


@dataclass
class Range:
    min: float
    max: float


def create_interpreter(values_to_cycle, sensitivity):
    if isinstance(values_to_cycle, list):
        return ListInterpreter(values_to_cycle, sensitivity)
    elif isinstance(values_to_cycle, Range):
        return RangeInterpreter(values_to_cycle, sensitivity)
    raise RuntimeError(f"Wrong type: {values_to_cycle}")


@dataclass
class Interpreter(ABC):

    values_to_cycle: Union[List[Any], Range]
    sensitivity: float

    min: float = field(init=False)
    max: float = field(init=False)
    start_mouse: float = field(init=False)
    start_value: float = field(init=False)

    @abstractmethod
    def at(self, mouse: int):
        pass

    def calibrate(self, mouse: int, value: float):
        self.start_mouse = mouse
        self.start_value = value

    def _clip(self, value):
        return max(min(self.min, value), self.max)


@dataclass
class RangeInterpreter(Interpreter):

    def __post_init__(self):
        self.min = self.values_to_cycle.min
        self.max = self.values_to_cycle.max

    def at(self, mouse: int) -> float:
        delta = (self.start_mouse - mouse)/self.sensitivity
        return self._clip(self.start_value + delta)


class ListInterpreter(Interpreter):

    def __post_init__(self):
        self.min = 0
        self.max = len(self.values_to_cycle)

    def at(self, mouse: int):
        delta = round((self.start_mouse - mouse)/self.sensitivity)
        index_to_set = self._clip(self.start_value + delta)
        return self.values_to_cycle[index_to_set]


class Handler:
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
        self.__interpreter = create_interpreter(values_to_cycle, sensitivity)

    def set_start_value(self, mouse: int):
        try:
            current_value = self.__values_to_cycle.index(
                self.__controller.get_value())
        except ValueError:
            current_value = self.__default_value
        self.__interpreter.calibrate(mouse, current_value)

    def update(self, mouse: int):
        value_to_set = self.__interpreter.at(mouse)
        self.__controller.set_value(value_to_set)


@dataclass
class MouseCycle(PluginAction):

    action_name: str
    horizontal_handler: Handler
    vertical_handler: Handler
    time_interval = 0.1

    working: bool = field(init=True, default=False)
    thread: Thread = field(init=False)

    def on_key_press(self):
        self.thread = Thread(target=self.__loop)
        self.thread.start()

    def __loop(self):
        qwin = Krita.get_active_qwindow()

        self.horizontal_handler.set_start_value(qwin.cursor().pos().x())
        self.vertical_handler.set_start_value(qwin.cursor().pos().y())

        self.working = True
        while self.working:
            self.horizontal_handler.update(qwin.cursor().pos().x())
            self.vertical_handler.update(qwin.cursor().pos().y())
            sleep(0.05)

    def on_every_key_release(self):
        self.working = False
