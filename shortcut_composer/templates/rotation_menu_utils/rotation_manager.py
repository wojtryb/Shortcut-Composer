# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
# FIXME: move to common
from shortcut_composer.core_components.controller_base import Controller
from templates.pie_menu_utils.pie_widget_utils import CirclePoints


class RotationManager:
    """
    Handles the passed PieWidget by tracking a mouse to find active label.

    - Displays the widget between start() and stop() calls.
    - Starts a thread loop which checks for changes of active label.
    """

    def __init__(
        self,
        controller: Controller[int],
        modifier: Callable[[int], int] = lambda x: x,
        deadzone: int = 100
    ):
        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())
        self._controller = controller
        self._modifier = modifier
        self._deadzone = deadzone

    def start(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        # self._pie_widget.move_center(QCursor().pos())
        # self._pie_widget.show()

        self._timer.start()
        self._center_global = QCursor().pos()
        self._starting_value = self._controller.get_value()

    def stop(self, hide: bool = True) -> None:
        """Hide the widget and stop the mouse tracking loop."""
        self._timer.stop()
        # if hide:
        #     self._pie_widget.hide()

    def _handle_cursor(self) -> None:
        """Calculate zone of the cursor and mark which child is active."""
        # NOTE: The widget can get hidden outside of stop() when key is
        # released during the drag&drop operation or when user clicked
        # outside the pie widget.
        # if not self._pie_widget.isVisible():
        #     return self.stop()

        # if self._pie_widget.is_in_edit_mode:
        #     return self.stop()

        cursor = QCursor().pos()
        circle = CirclePoints(self._center_global, 0)
        if circle.distance(cursor) > self._deadzone:
            to_set = self._modifier(int(circle.angle_from_point(cursor)))
        else:
            to_set = self._starting_value
        self._controller.set_value(to_set)

        # angle = circle.angle_from_point(cursor)
        # holder = self._pie_widget.order_handler.widget_holder
        # self._set_active_label(holder.on_angle(angle).label)

    # def _set_active_label(self, label: Optional[PieLabel]) -> None:
    #     """Mark label as active and start animating the change."""
    #     if self._pie_widget.active_label != label:
    #         self._pie_widget.active_label = label
    #         self._animator.start()
