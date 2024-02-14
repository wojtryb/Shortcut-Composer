# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita.pyqt import Painter

from .rotation_style import RotationStyle
from .rotation_widget_state import Zone, WidgetState


class RotationPainter:
    def __init__(self, style: RotationStyle):
        self._style = style

    def paint(self, painter: Painter, state: WidgetState):
        self._painter = painter
        self._state = state

        self._paint_deadzone_indicator()
        self._paint_free_zone_indicator()
        self._paint_active_angle()

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._style.widget_radius, self._style.widget_radius)

    def _paint_deadzone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""
        if not self._style.deadzone_radius:
            return

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.deadzone_radius,
            color=QColor(128, 255, 128, 120),
            thickness=1)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.deadzone_radius-1,
            color=QColor(255, 128, 128, 120),
            thickness=1)

    def _paint_free_zone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""
        if self._style.deadzone_radius == self._style.inner_zone_radius:
            return

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.inner_zone_radius,
            color=QColor(128, 255, 128, 120),
            thickness=1)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.inner_zone_radius-1,
            color=QColor(255, 128, 128, 120),
            thickness=1)

    def _paint_active_angle(self) -> None:
        thickness = self._style.inner_zone_radius-self._style.deadzone_radius+2
        for angle, progress in self._state.animations_in_progress.items():

            thickness_change = round(
                (1-progress.value) * self._style.transparent_border)

            color = self._style.active_color
            color.setAlpha(round(progress.value * 255))

            self._painter.paint_pie(
                center=self._center,
                outer_radius=self._style.inner_zone_radius+thickness_change,
                angle=angle,
                span=self._style.discrete_pie_span,
                color=color,
                thickness=thickness+thickness_change)

        if self._state.selected_zone == Zone.CONTIGUOUS_ZONE:
            self._painter.paint_pie(
                center=self._center,
                outer_radius=self._style.inner_zone_radius,
                angle=self._state.selected_angle,
                span=10,
                color=self._style.active_color,
                thickness=thickness)

        # +2 allows the indicator to cover the deadzone circle
