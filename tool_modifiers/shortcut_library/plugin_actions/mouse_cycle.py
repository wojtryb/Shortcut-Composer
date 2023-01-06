from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from threading import Thread
from time import sleep

from .krita_api_wrapper import Krita
from .interfaces import PluginAction
from .controllers import Controller


class TwoWayIterator(ABC):
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def previous(self):
        pass


class ActionIterator(TwoWayIterator):
    def next(self):
        Krita.trigger_action("next_favorite_preset")
        # Krita.trigger_action("KritaShape/KisToolBrush")

    def previous(self):
        Krita.trigger_action("previous_favorite_preset")
        # Krita.trigger_action("KisToolSelectOutline")


class Handler:
    # def __init__(self, controller: Controller, prev_next: TwoWayIterator):
    #     self.__controller = controller
    #     self.__two_way_iterator = prev_next
    def __init__(self):
        self.__controller = Controller()
        self.__two_way_iterator = ActionIterator()

        self.__start_value = 0
        self.__step = 50

    def set_start_value(self, value: int):
        self.__start_value = value

    def update(self, current_value):
        if current_value > self.__start_value + self.__step:
            self.__controller.set_value(self.__two_way_iterator.next())
            self.__start_value = current_value + self.__step

        elif current_value < self.__start_value - self.__step:
            self.__controller.set_value(self.__two_way_iterator.previous())
            self.__start_value = current_value - self.__step


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
            # print(qwin.cursor().pos().x())
            sleep(0.05)

    def on_every_key_release(self):
        self.working = False
