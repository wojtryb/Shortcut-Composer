import math
from threading import Thread
from typing import Optional

from .pie_widget import PieWidget
from .label import Label
from .label_holder import LabelHolder
from api_krita import Krita
from time import sleep
from shortcut_composer_config import FPS_LIMIT, PIE_DEADZONE_PX


class PieManager:
    def __init__(self, widget: PieWidget, labels: LabelHolder) -> None:
        self._widget = widget
        self._labels = labels
        self._is_working = False
        self._sleep_time = 1/FPS_LIMIT if FPS_LIMIT else 0.001

    def start(self):
        self._is_working = True
        Thread(target=self._track_angle, daemon=True).start()

    def stop(self):
        self._is_working = False

    def _track_angle(self):
        self._cursor = Krita.get_cursor()
        while self._is_working:
            if self._distance_from_center() < PIE_DEADZONE_PX:
                self._set_active_label(None)
            else:
                angle = self._angle_from_cursor()
                label = self._labels.from_angle(round(angle))
                self._set_active_label(label)
            sleep(self._sleep_time)

    def _distance_from_center(self):
        return (
            (self._widget.center_global.x() - self._cursor.x()) ** 2
            + (self._widget.center_global.y() - self._cursor.y()) ** 2
        ) ** 0.5

    def _angle_from_cursor(self):
        angle = math.degrees(math.atan2(
            -self._widget.center_global.x() + self._cursor.x(),
            self._widget.center_global.y() - self._cursor.y()
        ))
        return angle % 360

    def _set_active_label(self, label: Optional[Label]):
        if self._labels.active != label:
            self._labels.active = label
            self._widget.repaint()
