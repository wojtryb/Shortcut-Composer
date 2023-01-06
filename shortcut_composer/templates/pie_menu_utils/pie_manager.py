# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Thread
from typing import Optional
from time import sleep

from PyQt5.QtGui import QCursor

from composer_utils import Config
from .pie_widget import PieWidget
from .label import Label
from .circle_points import CirclePoints


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
        self._sleep_time = Config.get_sleep_time()

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
        circle = CirclePoints(self._widget.center_global, 0)
        while self._is_working:
            cursor = QCursor().pos()
            if circle.distance(cursor) < self._widget.deadzone:
                label = None
            else:
                angle = circle.angle_from_point(cursor)
                label = self._widget.labels.from_angle(round(angle))
            self._set_active_label(label)
            sleep(self._sleep_time)

    def _set_active_label(self, label: Optional[Label]):
        """Mark label as active and ask the widget to repaint."""
        if self._widget.labels.active != label:
            self._widget.labels.active = label
            self._widget.repaint()
