# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
# FIXME: move to common
from shortcut_composer.core_components.controller_base import Controller
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
        config: RotationConfig,
        controller: Controller[int],
        modifier: Callable[[int], int] = lambda x: x,
    ):
        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())
        self._controller = controller
        self._modifier = modifier
        self._config = config

        self._rotation_widget = RotationWidget(config=self._config)

    def start(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        self._rotation_widget.move_center(QCursor().pos())
        self._rotation_widget.show()

        self._timer.start()
        self._center_global = QCursor().pos()
        self._starting_value = self._controller.get_value()

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

        def snap_angle():
            return self._modifier(snap_degree(
                value=round(circle.angle_from_point(cursor)),
                step_size=360//self._config.DIVISIONS.read()))

        def free_angle():
            return self._modifier(round(circle.angle_from_point(cursor)))

        inner_zone = snap_angle
        outer_zone = free_angle
        if self._config.INVERSE_ZONES.read():
            inner_zone, outer_zone = outer_zone, inner_zone

        if circle.distance(cursor) < self._config.deadzone_radius:
            to_set = self._starting_value
        elif circle.distance(cursor) < self._config.widget_radius:
            to_set = inner_zone()
        else:
            to_set = outer_zone()

        self._controller.set_value(to_set)
