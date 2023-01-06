from dataclasses import dataclass, field
from threading import Thread
from time import sleep

from .krita_api_wrapper import Krita
from .interfaces import PluginAction


@dataclass
class MouseCycle(PluginAction):

    action_name: str
    time_interval = 0.1
    working: bool = field(init=True, default=False)
    thread: Thread = field(init=False)

    def on_key_press(self):
        self.thread = Thread(target=self.__loop)
        self.thread.start()

    def __loop(self):
        qwin = Krita.get_active_qwindow()
        self.working = True
        while self.working:
            print(qwin.cursor().pos())
            sleep(0.05)

    def on_every_key_release(self):
        self.working = False
