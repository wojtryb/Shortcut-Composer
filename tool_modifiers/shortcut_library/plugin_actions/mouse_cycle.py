from dataclasses import dataclass, field
from threading import Thread
from time import sleep
from typing import Union

from .krita_api_wrapper import Krita
from .interfaces import PluginAction


@dataclass
class Range:
    min: float
    max: float


class ValueInterpreter:
    def __init__(
        self,
        values_to_cycle: Union[list, Range],
        sensitivity: float
    ):
        if isinstance(values_to_cycle, list):
            self.min = 0
            self.max = len(values_to_cycle) * sensitivity
            self.map = {i*sensitivity: value
                        for i, value in enumerate(values_to_cycle)}
        elif isinstance(values_to_cycle, Range):
            self.min = values_to_cycle.min
            self.max = values_to_cycle.max
        else:
            raise RuntimeError(f"Wrong type: {values_to_cycle}")

    def __getitem__(self, item):
        for key, value in reversed(self.map.items()):
            if item >= key:
                return value
        return value


class Handler:
    def __init__(self, controller,  values_to_cycle, sensitivity=50):
        self.__controller = controller
        self.__interpreter = ValueInterpreter(values_to_cycle, sensitivity)
        self.__current_value = 0

    def set_start_value(self, mouse_value: int):
        self.__start_value = mouse_value - self.__current_value

    def update(self, mouse_value: int):
        self.__current_value = mouse_value - self.__start_value
        to_set = self.__interpreter[self.__current_value]
        self.__controller.set_value(to_set)

        print(self.__current_value)

        if self.__current_value < self.__interpreter.min:
            self.__start_value -= self.__interpreter.min - self.__current_value
        elif self.__current_value > self.__interpreter.max:
            self.__start_value += self.__current_value - self.__interpreter.max


@ dataclass
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
