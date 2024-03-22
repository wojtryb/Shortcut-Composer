# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita.pyqt import Painter
from ..rotation_style import RotationStyle
from .rotation_widget_state import Zone, WidgetState


class RotationPainter:
    """Uses provided painter and parts of widget information to paint it."""

    def __init__(self, style: RotationStyle) -> None:
        self._style = style

    def paint(self, painter: Painter, state: WidgetState) -> None:
        """Paint the widget which created the passed painter."""
        self._painter = painter
        self._state = state

        self._paint_deadzone_indicator()
        self._paint_free_zone_indicator()
        self._paint_selection()

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._style.widget_radius, self._style.widget_radius)

    def _paint_deadzone_indicator(self) -> None:
        """Paint the circle representing deadzone."""
        if not self._style.deadzone_radius:
            return

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.deadzone_radius,
            color=QColor(255, 128, 128, self._style.outline_opacity),
            thickness=2)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.deadzone_radius-2,
            color=QColor(128, 255, 128, self._style.outline_opacity),
            thickness=2)

    def _paint_free_zone_indicator(self) -> None:
        """Paint the circle representing zone after deadzone."""
        if self._style.deadzone_radius == self._style.inner_zone_radius:
            return

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.inner_zone_radius,
            color=QColor(128, 255, 128, self._style.outline_opacity),
            thickness=2)

        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.inner_zone_radius-2,
            color=QColor(255, 128, 128, self._style.outline_opacity),
            thickness=2)

    def _paint_selection(self) -> None:
        """Paint pies representing selected value."""
        for angle, progress in self._state.animations_in_progress.items():
            if progress.value == 0:
                continue
            self._paint_decorated_pie(
                angle=angle,
                span=self._style.intervallic_pie_span,
                animation_value=progress.value)

        if self._state.selected_zone == Zone.PRECISE_ZONE:
            self._paint_decorated_pie(
                angle=self._state.selected_angle,
                span=self._style.precise_pie_span,
                animation_value=1.0)

    def _paint_decorated_pie(
        self,
        angle: int,
        span: int,
        animation_value: float,
    ) -> None:
        """Paint a pie with decorator and border."""
        thickness = self._style.inner_zone_radius-self._style.deadzone_radius+2
        # +2 allows the indicator to cover the deadzone circle

        thickness_change = round(
            (1-animation_value) * self._style.transparent_border)

        # two outlines on both sides
        self._painter.paint_pie(
            center=self._center,
            outer_radius=self._style.inner_zone_radius+thickness_change-2,
            angle=angle,
            span=span+4,  # Add 2 degrees on each side
            color=self._scale_opacity(
                QColor(255, 128, 128, self._style.outline_opacity),
                animation_value),
            thickness=thickness+thickness_change-2)

        self._painter.paint_pie(
            center=self._center,
            outer_radius=self._style.inner_zone_radius+thickness_change,
            angle=angle,
            span=span+2,  # Add 1 degree on each side
            color=self._scale_opacity(
                QColor(128, 255, 128, self._style.outline_opacity),
                animation_value),
            thickness=thickness+thickness_change)

        # indicator base
        self._painter.paint_pie(
            center=self._center,
            outer_radius=self._style.inner_zone_radius+thickness_change,
            angle=angle,
            span=span,
            color=self._scale_opacity(
                self._style.active_color, animation_value),
            thickness=thickness+thickness_change+2)

        # indicator decorator
        self._painter.paint_pie(
            center=self._center,
            outer_radius=self._style.inner_zone_radius+thickness_change,
            angle=angle,
            span=span,
            color=self._scale_opacity(
                self._style.active_color_dark, animation_value),
            thickness=self._style.decorator_thickness)

        # indicator top border
        self._painter.paint_pie(
            center=self._center,
            outer_radius=self._style.inner_zone_radius+thickness_change+1,
            angle=angle,
            span=span,
            color=self._scale_opacity(
                self._style.border_color, animation_value),
            thickness=self._style.border_thickness)

    @staticmethod
    def _scale_opacity(color: QColor, scale: float) -> QColor:
        """Return QColor with modified opacity."""
        opacity = round(scale * color.alpha())
        return QColor(color.red(), color.green(), color.blue(), opacity)
