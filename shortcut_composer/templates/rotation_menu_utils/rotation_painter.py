# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita.pyqt import Painter

from .zone import Zone


class RotationPainter:
    def __init__(
        self,
        painter: Painter,
        deadzone_radius: int,
        widget_radius: int,
        selected_angle: int,
        selected_zone: Zone,
        divisions: int,
        active_color: QColor,
    ):
        self._painter = painter
        self._deadzone_radius = deadzone_radius
        self._widget_radius = widget_radius
        self._selected_angle = selected_angle
        self._selected_zone = selected_zone
        self._divisions = divisions
        self._active_color = active_color

        self._paint_deadzone_indicator()
        self._paint_free_zone_indicator()
        self._paint_active_angle()

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._widget_radius, self._widget_radius)

    def _paint_deadzone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""
        if not self._deadzone_radius:
            return

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._deadzone_radius,
            color=QColor(128, 255, 128, 120),
            thickness=1)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._deadzone_radius-1,
            color=QColor(255, 128, 128, 120),
            thickness=1)

    def _paint_free_zone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""
        if self._deadzone_radius == self._widget_radius:
            return

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._widget_radius,
            color=QColor(128, 255, 128, 120),
            thickness=1)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._widget_radius-1,
            color=QColor(255, 128, 128, 120),
            thickness=1)

    def _paint_active_angle(self) -> None:
        if self._selected_zone == Zone.DEADZONE:
            return

        if self._selected_zone == Zone.DISCRETE_ZONE:
            span = 360//self._divisions
        else:
            span = 10

        self._painter.paint_pie(
            center=self._center,
            outer_radius=self._widget_radius,
            angle=self._selected_angle,
            span=span,
            color=self._active_color,
            thickness=self._widget_radius-self._deadzone_radius+2)
        # +2 allows the indicator to cover the deadzone circle
