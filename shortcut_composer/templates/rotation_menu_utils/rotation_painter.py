# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita.pyqt import Painter


class RotationPainter:
    def __init__(
        self,
        painter: Painter,
        deadzone_radius: int,
        widget_radius: int,
    ):
        self._painter = painter
        self._deadzone_radius = deadzone_radius
        self._widget_radius = widget_radius
        self._paint_deadzone_indicator()
        self._paint_free_zone_indicator()

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._widget_radius, self._widget_radius)

    def _paint_deadzone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._deadzone_radius,
            color=QColor(128, 255, 128, 120),
            thickness=1)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._deadzone_radius,
            color=QColor(255, 128, 128, 120),
            thickness=1)

    def _paint_free_zone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._widget_radius,
            color=QColor(128, 255, 128, 120),
            thickness=1)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._widget_radius,
            color=QColor(255, 128, 128, 120),
            thickness=1)
