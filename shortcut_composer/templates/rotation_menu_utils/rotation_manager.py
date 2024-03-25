# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import CirclePoints, Config
from .rotation_widget import RotationWidget
from .rotation_config import RotationConfig
from .rotation_style import RotationStyle
from .rotation_widget_utils import Zone


class RotationManager:
    """
    Updates the state of RotationWidget by tracking a mouse.

    Displays the widget and tracks a mouse between start() and stop() calls.
    Contiguously updates widget state, updates animations and paints it.
    """

    def __init__(
        self,
        rotation_widget: RotationWidget,
        config: RotationConfig,
        style: RotationStyle,
    ) -> None:
        self._rotation_widget = rotation_widget
        self._config = config
        self._style = style

        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())

    def start(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        if not self._config.IS_WIDGET_HIDDEN.read():
            self._rotation_widget.move_center(QCursor().pos())
            self._rotation_widget.show()

        self._center_global = QCursor().pos()
        self._rotation_widget.state.reset()

        self._timer.start()

    def stop(self, hide: bool = True) -> None:
        """Hide the widget and stop the mouse tracking loop."""
        self._timer.stop()
        if hide:
            self._rotation_widget.hide()

    def _handle_cursor(self) -> None:
        """Calculate zone and angle of the cursor."""
        cursor = QCursor().pos()
        circle = CirclePoints(self._center_global, 0)

        is_inverse = self._config.INVERSE_ZONES.read()
        if circle.distance(cursor) < self._style.deadzone_radius:
            zone = Zone.DEADZONE
        elif circle.distance(cursor) < self._style.inner_zone_radius:
            zone = Zone.PRECISE_ZONE if is_inverse else Zone.INTERVALLIC_ZONE
        else:
            zone = Zone.INTERVALLIC_ZONE if is_inverse else Zone.PRECISE_ZONE
        self._rotation_widget.state.selected_zone = zone

        angle = round(circle.angle_from_point(cursor))
        if zone == Zone.INTERVALLIC_ZONE:
            angle = self._snap_degree(
                value=angle,
                step_size=self._style.intervallic_pie_span)
        self._rotation_widget.state.selected_angle = angle

        self._rotation_widget.state.tick_animations()
        self._rotation_widget.repaint()

    @staticmethod
    def _snap_degree(value: int, step_size: int) -> int:
        """Snap a `value` to closest multiplication of the `step_size`"""
        if not 0 < step_size <= 360:
            raise RuntimeError("Step needs to be in range (0, 360>")

        moved_by_half_of_step = value + step_size//2
        snapped = moved_by_half_of_step // step_size * step_size

        return snapped % 360
