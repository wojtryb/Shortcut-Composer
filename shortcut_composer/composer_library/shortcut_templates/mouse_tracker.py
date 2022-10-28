from dataclasses import dataclass

from time import sleep
from typing import Optional

from ..krita_api import Krita
from ..shortcut_connection_utils import PluginAction
from .slider_utils import Slider


@dataclass
class MouseTracker(PluginAction):

    action_name: str
    horizontal_slider: Optional[Slider] = None
    vertical_slider: Optional[Slider] = None

    time_interval = 0.1
    working = False

    def on_key_press(self) -> None:
        self.working = True
        cursor = Krita.get_cursor()

        if self.horizontal_slider and not self.vertical_slider:
            return self.horizontal_slider.start(cursor.x)
        if not self.horizontal_slider and self.vertical_slider:
            return self.vertical_slider.start(lambda: -cursor.y())

        start_point = (cursor.x(), cursor.y())
        while self.working:
            delta_hor = abs(start_point[0] - cursor.x())
            delta_ver = abs(start_point[1] - cursor.y())
            if abs(delta_hor - delta_ver) >= 10:
                break
            sleep(0.05)

        if delta_hor > delta_ver:
            self.horizontal_slider.start(cursor.x)
        else:
            self.vertical_slider.start(lambda: -cursor.y())

    def on_every_key_release(self) -> None:
        self.working = False
        if self.horizontal_slider:
            self.horizontal_slider.stop()
        if self.vertical_slider:
            self.vertical_slider.stop()
