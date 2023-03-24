# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
from .scroll_area import ScrollArea
from .pie_widget import PieWidget
from .label_widget import LabelWidget
from .widget_utils import CirclePoints


class PieManager:
    """
    Handles the passed PieWidget by tracking a mouse to find active label.

    - Displays the widget between start() and stop() calls.
    - Starts a thread loop which checks for changes of active label.
    - Asks the widget to repaint when after changing active label.
    """

    def __init__(self, widget: PieWidget, pie_settings: ScrollArea) -> None:
        self._pie = widget
        self._pie_settings = pie_settings
        self._holder = self._pie.widget_holder
        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())
        self._animator = LabelAnimator(widget)

        self._circle: CirclePoints

    def start(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        self._pie.move_center(QCursor().pos())
        self._pie_settings.move_to_pie_side()
        self._pie.show()
        self._circle = CirclePoints(self._pie.center_global, 0)
        self._timer.start()

    def stop(self) -> None:
        """Hide the widget and stop the mouse tracking loop."""
        self._timer.stop()
        for label in self._pie.labels:
            label.activation_progress.reset()
        self._pie.hide()

    def _handle_cursor(self) -> None:
        """Calculate zone of the cursor and mark which child is active."""
        # NOTE: The widget can get hidden outside of stop() when key is
        # released during the drag&drop operation or when user clicked
        # outside the pie widget.
        if not self._pie.isVisible():
            return self.stop()

        cursor = QCursor().pos()
        if self._circle.distance(cursor) < self._pie.deadzone:
            return self._set_active_widget(None)

        angle = self._circle.angle_from_point(cursor)
        self._set_active_widget(self._holder.on_angle(angle))

    def _set_active_widget(self, widget: Optional[LabelWidget]) -> None:
        """Mark label as active and start animating the change."""
        if self._holder.active != widget:
            self._holder.active = widget
            self._animator.start()


class LabelAnimator:
    """
    Controls the animation of background under pie labels.

    Handles the whole widget at once, to prevent unnecessary repaints.
    """

    def __init__(self, widget: PieWidget) -> None:
        self._widget = widget
        self._children = widget.widget_holder
        self._timer = Timer(self._update, Config.get_sleep_time())

    def start(self) -> None:
        """Start animating. The animation will stop automatically."""
        self._timer.start()

    def _update(self) -> None:
        """Move all labels to next animation state. End animation if needed."""
        for widget in self._children:
            if self._children.active == widget:
                widget.label.activation_progress.up()
            else:
                widget.label.activation_progress.down()

        self._widget.repaint()
        for widget in self._children:
            if widget.label.activation_progress.value not in (0, 1):
                return
        self._timer.stop()
