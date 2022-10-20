from dataclasses import dataclass, field

from threading import Thread
from time import sleep

from ..api_adapter import Krita
from ..plugin_action_utils import PluginAction
from .slider_utils import Slider, EmptySlider


@dataclass
class VirtualSliderAction(PluginAction):

    action_name: str
    horizontal_slider: Slider = field(default_factory=EmptySlider)
    vertical_slider: Slider = field(default_factory=EmptySlider)
    separate_sliders: bool = True
    time_interval = 0.1

    def __post_init__(self):
        self.working = False
        self.thread: Thread

    @property
    def is_single_mode(self):
        return (isinstance(self.horizontal_slider, EmptySlider)
                or isinstance(self.vertical_slider, EmptySlider))

    def on_key_press(self):
        if self.separate_sliders and not self.is_single_mode:
            target = self._loop_separate
        else:
            target = self._loop_common
        self.thread = Thread(target=target, daemon=True)
        self.thread.start()

    def _loop_common(self):
        cursor = Krita.get_cursor()

        self.horizontal_slider.set_start_value(cursor.x)
        self.vertical_slider.set_start_value(-cursor.y)

        self.working = True
        while self.working:
            self.horizontal_slider.handle(cursor.x)
            self.vertical_slider.handle(-cursor.y)
            sleep(0.05)

    def _loop_separate(self):
        cursor = Krita.get_cursor()

        self.horizontal_slider.set_start_value(cursor.x)
        self.vertical_slider.set_start_value(-cursor.y)

        self.working = True
        while self.working:
            delta_hor = abs(self.horizontal_slider.mouse.start - cursor.x)
            delta_ver = abs(self.vertical_slider.mouse.start + cursor.y)
            if abs(delta_hor - delta_ver) >= 10:
                break
            sleep(0.05)

        if delta_hor > delta_ver:
            while self.working:
                to_set_x = cursor.x
                self.horizontal_slider.handle(to_set_x)
                sleep(0.05)
        else:
            while self.working:
                to_set_y = cursor.y
                self.vertical_slider.handle(-to_set_y)
                sleep(0.05)

    def on_every_key_release(self):
        self.working = False
