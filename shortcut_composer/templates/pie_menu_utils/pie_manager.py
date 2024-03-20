# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import CirclePoints, Config
from .pie_label import PieLabel
from .pie_widget import PieWidget


class PieManager:
    """
    Handles the passed PieWidget by tracking a mouse to find active label.

    Displays the widget between start() and stop() calls.
    """

    def __init__(self, pie_widget: PieWidget) -> None:
        self._pie_widget = pie_widget
        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())
        self._animator = LabelAnimator(pie_widget)

    def start(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        self._pie_widget.move_center(QCursor().pos())
        self._pie_widget.show()

        self._timer.start()

        # Make sure the pie widget is not draggable. It could have been
        # broken by pie settings reloading the widgets.
        self._pie_widget.set_draggable(False)

    def stop(self, hide: bool = True) -> None:
        """Hide the widget and stop the mouse tracking loop."""
        self._pie_widget.active_label = None
        self._timer.stop()
        for label in self._pie_widget.order_handler:
            label.activation_progress.reset()
        if hide:
            self._pie_widget.hide()

    def _handle_cursor(self) -> None:
        """Calculate zone of the cursor and mark which child is active."""
        # NOTE: The widget can get hidden outside of stop() when key is
        # released during the drag&drop operation or when user clicked
        # outside the pie widget.
        if not self._pie_widget.isVisible():
            return self.stop()

        if self._pie_widget.is_in_edit_mode:
            return self.stop()

        if not self._pie_widget.order_handler:
            return

        cursor = QCursor().pos()
        circle = CirclePoints(self._pie_widget.center_global, 0)
        if circle.distance(cursor) < self._pie_widget.deadzone:
            return self._set_active_label(None)

        angle = circle.angle_from_point(cursor)
        holder = self._pie_widget.order_handler.widget_holder
        self._set_active_label(holder.on_angle(angle).label)

    def _set_active_label(self, label: PieLabel | None) -> None:
        """Mark label as active and start animating the change."""
        if self._pie_widget.active_label != label:
            self._pie_widget.active_label = label
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
        for label in self._pie_widget.order_handler:
            if self._pie_widget.active_label == label:
                label.activation_progress.up()
            else:
                label.activation_progress.down()

        self._pie_widget.repaint()
        for label in self._pie_widget.order_handler:
            if label.activation_progress.value not in (0, 1):
                return
        self._timer.stop()
