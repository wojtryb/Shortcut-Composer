# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
from .pie_widget import PieWidget
from .label_widgets import LabelWidget
from .circle_points import CirclePoints
from .label_animator import LabelAnimator


class PieManager:
    """
    Handles the passed PieWidget by tracking a mouse to find active label.

    - Displays the widget between start() and stop() calls.
    - Starts a thread loop which checks for changes of active label.
    - Asks the widget to repaint when after changing active label.
    """

    def __init__(self, widget: PieWidget) -> None:
        self._widget = widget
        self._holder = self._widget.widget_holder
        self._timer = Timer(self._track_angle, Config.get_sleep_time())
        self._animator = LabelAnimator(widget)

        self._circle: CirclePoints

    def start(self):
        """Show widget under the mouse and start the mouse tracking loop."""
        self._widget.move_center(QCursor().pos())
        self._widget.show()
        self._circle = CirclePoints(self._widget.center_global, 0)
        self._timer.start()

    def stop(self):
        """Hide the widget and stop the mouse tracking loop."""
        self._timer.stop()
        for label in self._widget.labels:
            label.activation_progress.reset()
        self._widget.hide()

    def _track_angle(self):
        """Block a thread contiguously setting an active label."""
        cursor = QCursor().pos()
        if self._circle.distance(cursor) < self._widget.deadzone:
            return self._set_active_widget(None)

        angle = self._circle.angle_from_point(cursor)
        self._set_active_widget(self._holder.on_angle(angle))

    def _set_active_widget(self, widget: Optional[LabelWidget]):
        """Mark label as active and start animating the change."""
        if self._holder.active != widget:
            self._holder.active = widget
            self._animator.start()
