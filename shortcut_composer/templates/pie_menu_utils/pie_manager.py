import math
from threading import Thread

from .pie_widget import PieWidget
from .label import Label
from .label_holder import LabelHolder
from api_krita import Krita
from time import sleep
from shortcut_composer_config import FPS_LIMIT


class PieManager:
    def __init__(self, widget: PieWidget, labels: LabelHolder) -> None:
        self._widget = widget
        self._labels = labels
        self._is_working = False
        self._sleep_time = 1/FPS_LIMIT if FPS_LIMIT else 0.001

    def start_loop(self):
        self._is_working = True
        Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while self._is_working:
            angle = self.angle_from_cursor()
            label = self._labels.from_angle(round(angle))
            self.set_active_label(label)
            sleep(self._sleep_time)

    def angle_from_cursor(self):
        cursor = Krita.get_cursor()
        angle = math.degrees(math.atan2(
            -self._widget.center_global.x() + cursor.x(),
            self._widget.center_global.y() - cursor.y()
        ))
        return angle % 360

    def set_active_label(self, label: Label):
        if self._labels.active != label:
            self._labels.active = label
            self._widget.changed = True
            self._widget.repaint()

    def stop(self):
        self._is_working = False
