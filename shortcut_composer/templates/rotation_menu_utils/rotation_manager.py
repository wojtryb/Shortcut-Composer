# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

# from typing import Callable

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
# FIXME: move to common
# from shortcut_composer.core_components.controller_base import Controller
from templates.pie_menu_utils.pie_widget_utils import CirclePoints
from .rotation_widget import RotationWidget
from .rotation_config import RotationConfig


def snap_degree(value: int, step_size: int) -> int:
    if not 0 < step_size <= 360:
        raise RuntimeError("Step needs to be in range (0, 360>")

    moved_by_half_of_step = value + step_size//2
    snapped = moved_by_half_of_step // step_size * step_size

    return snapped % 360


class RotationManager:
    """
    Handles the passed PieWidget by tracking a mouse to find active label.

    - Displays the widget between start() and stop() calls.
    - Starts a thread loop which checks for changes of active label.
    """

    def __init__(
        self,
        rotation_widget: RotationWidget,
        config: RotationConfig
    ) -> None:
        self._rotation_widget = rotation_widget
        self._config = config

        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())

    def start(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        self._rotation_widget.move_center(QCursor().pos())
        self._rotation_widget.show()

        self._center_global = QCursor().pos()
        self._rotation_widget.reset_state()

        self._timer.start()

    def stop(self, hide: bool = True) -> None:
        """Hide the widget and stop the mouse tracking loop."""
        self._timer.stop()
        if hide:
            self._rotation_widget.hide()

    def _handle_cursor(self) -> None:
        """Calculate zone of the cursor and mark which child is active."""
        # NOTE: The widget can get hidden outside of stop() when key is
        # released during the drag&drop operation or when user clicked
        # outside the pie widget.
        if not self._rotation_widget.isVisible():
            return self.stop()

        cursor = QCursor().pos()
        circle = CirclePoints(self._center_global, 0)

        self._rotation_widget.selected_angle = round(
            circle.angle_from_point(cursor))

        if circle.distance(cursor) < self._config.deadzone_radius:
            zone = RotationWidget.Zone.DEADZONE
        elif circle.distance(cursor) < self._config.widget_radius:
            zone = RotationWidget.Zone.INNER_ZONE
        else:
            zone = RotationWidget.Zone.OUTER_ZONE

        self._rotation_widget.selected_zone = zone
