import math
from threading import Thread
from typing import Optional
from time import sleep

from PyQt5.QtGui import QCursor

from shortcut_composer_config import FPS_LIMIT
from api_krita import Krita
from api_krita.wrappers import Cursor
from .pie_widget import PieWidget
from .label import Label


class PieManager:
    """
    Handles the passed PieWidget by tracking a mouse to find active label.

    - Displays the widget between start() and stop() calls.
    - Starts a thread loop which checks for changes of active label.
    - Asks the widget to repaint when after changing active label.
    """

    def __init__(self, widget: PieWidget) -> None:
        self._widget = widget
        self._is_working = False
        self._sleep_time = 1/FPS_LIMIT if FPS_LIMIT else 0.001

        self._cursor: Cursor

    def start(self):
        """Show widget under the mouse and start the mouse tracking loop."""
        self._is_working = True
        self._widget.move_center(QCursor().pos())
        self._widget.show()
        Thread(target=self._track_angle, daemon=True).start()

    def stop(self):
        """Hide the widget and stop the mouse tracking loop."""
        self._widget.hide()
        self._is_working = False

    def _track_angle(self):
        """Block a thread contiguously setting an active label."""
        self._cursor = Krita.get_cursor()
        while self._is_working:
            if self._distance_from_center() < self._widget.deadzone:
                label = None
            else:
                angle = self._angle_from_cursor()
                label = self._widget.labels.from_angle(round(angle))
            self._set_active_label(label)
            sleep(self._sleep_time)

    def _distance_from_center(self):
        """Count distance between pie center and cursor position."""
        distance = (self._widget.center_global.x() - self._cursor.x()) ** 2
        distance += (self._widget.center_global.y() - self._cursor.y()) ** 2
        return distance ** 0.5

    def _angle_from_cursor(self):
        """Count clockwise angle of cursor in relation to pie center."""
        return math.degrees(math.atan2(
            -self._widget.center_global.x() + self._cursor.x(),
            self._widget.center_global.y() - self._cursor.y()
        )) % 360

    def _set_active_label(self, label: Optional[Label]):
        """Mark label as active and ask the widget to repaint."""
        if self._widget.labels.active != label:
            self._widget.labels.active = label
            self._widget.repaint()
