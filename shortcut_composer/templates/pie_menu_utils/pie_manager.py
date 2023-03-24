# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils.config import Config
from .settings_gui import PieSettings
from .pie_widget import PieWidget
from .label import Label
from .widget_utils import CirclePoints


class PieManager:
    """
    Handles the passed PieWidget by tracking a mouse to find active label.

    - Displays the widget between start() and stop() calls.
    - Starts a thread loop which checks for changes of active label.
    - Asks the widget to repaint when after changing active label.
    """

    def __init__(self, pie_widget: PieWidget, pie_settings: PieSettings):
        self._pie_widget = pie_widget
        self._pie_settings = pie_settings
        self._holder = pie_widget.aggregator.widget_holder
        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())
        self._animator = LabelAnimator(pie_widget)

        self._circle: CirclePoints

    def start(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        self._pie_widget.move_center(QCursor().pos())
        self._pie_widget.show()

        self._pie_settings.move_to_pie_side()
        self._circle = CirclePoints(self._pie_widget.center_global, 0)
        self._timer.start()

    def stop(self) -> None:
        """Hide the widget and stop the mouse tracking loop."""
        self._pie_widget.hide()
        self._timer.stop()
        for label in self._pie_widget.aggregator:
            label.activation_progress.reset()

    def _handle_cursor(self) -> None:
        """Calculate zone of the cursor and mark which child is active."""
        # NOTE: The widget can get hidden outside of stop() when key is
        # released during the drag&drop operation or when user clicked
        # outside the pie widget.
        if not self._pie_widget.isVisible():
            return self.stop()

        cursor = QCursor().pos()
        if self._circle.distance(cursor) < self._pie_widget.deadzone:
            return self._set_active_label(None)

        angle = self._circle.angle_from_point(cursor)
        self._set_active_label(self._holder.on_angle(angle).label)

    def _set_active_label(self, label: Optional[Label]) -> None:
        """Mark label as active and start animating the change."""
        if self._pie_widget.active != label:
            self._pie_widget.active = label
            self._animator.start()


class LabelAnimator:
    """
    Controls the animation of background under pie labels.

    Handles the whole widget at once, to prevent unnecessary repaints.
    """

    def __init__(self, pie_widget: PieWidget) -> None:
        self._pie_widget = pie_widget
        self._timer = Timer(self._update, Config.get_sleep_time())

    def start(self) -> None:
        """Start animating. The animation will stop automatically."""
        self._timer.start()

    def _update(self) -> None:
        """Move all labels to next animation state. End animation if needed."""
        for label in self._pie_widget.aggregator:
            if self._pie_widget.active == label:
                label.activation_progress.up()
            else:
                label.activation_progress.down()

        self._pie_widget.repaint()
        for label in self._pie_widget.aggregator:
            if label.activation_progress.value not in (0, 1):
                return
        self._timer.stop()
