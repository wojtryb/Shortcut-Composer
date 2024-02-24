# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita.pyqt import Painter
from ..pie_style import PieStyle
from ..pie_label import PieLabel


class PiePainter:
    """Uses provided painter and parts of widget information to paint it."""

    def __init__(self, style: PieStyle) -> None:
        self._style = style

    def paint(self, painter: Painter, labels: list[PieLabel]) -> None:
        """Paint the widget which created the passed painter."""
        self._painter = painter
        self._labels = labels

        self._paint_deadzone_indicator()
        self._paint_base_wheel()
        self._paint_active_pie()

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._style.widget_radius, self._style.widget_radius)

    def _paint_deadzone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""
        if self._style.deadzone_radius == float("inf"):
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

    def _paint_base_wheel(self) -> None:
        """Paint a base circle."""
        # NOTE: Windows10 does not treat the transparent center as part
        # of the widget, so a low opacity circle allows to trick it.
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.widget_radius,
            color=QColor(128, 128, 128, 1))

        # base wheel
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.pie_radius,
            color=self._style.background_color,
            thickness=self._style.area_thickness
            + self._style.border_thickness//2)

        # base wheel border
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.inner_edge_radius,
            color=self._style.border_color,
            thickness=self._style.border_thickness)

        # base wheel decorator
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=(
                self._style.inner_edge_radius
                + self._style.decorator_thickness),
            color=self._style.background_decorator_color,
            thickness=self._style.decorator_thickness)

    def _paint_active_pie(self) -> None:
        """Paint a pie behind a label which is active or during animation."""
        for label in self._labels:
            if not label.activation_progress.value:
                continue

            thickness_addition = round(
                0.15 * label.activation_progress.value
                * self._style.area_thickness)

            # active pie
            self._painter.paint_pie(
                center=self._center,
                outer_radius=self._style.pie_radius + thickness_addition,
                angle=label.angle,
                span=360//len(self._labels),
                color=self._pick_pie_color(label),
                thickness=self._style.area_thickness + thickness_addition)

            # pie decorator
            self._painter.paint_pie(
                center=self._center,
                outer_radius=self._style.pie_radius + thickness_addition,
                angle=label.angle,
                span=360//len(self._labels),
                color=self._style.pie_decorator_color,
                thickness=self._style.border_thickness*4)

            # active pie border
            self._painter.paint_pie(
                center=self._center,
                outer_radius=self._style.pie_radius +
                thickness_addition + self._style.border_thickness//2,
                angle=label.angle,
                span=360//len(self._labels),
                color=self._style.active_color_dark,
                thickness=self._style.border_thickness)

    def _pick_pie_color(self, label: PieLabel) -> QColor:
        """Pick color of pie based on widget mode and animation progress."""
        return self._overlay_colors(
            self._style.active_color_dark,
            self._style.active_color,
            opacity=label.activation_progress.value)

    @staticmethod
    def _overlay_colors(base: QColor, over: QColor, opacity: float) -> QColor:
        """Merge two colors by overlaying one on another with given opacity."""
        opacity_negation = 1-opacity
        return QColor(
            round(base.red()*opacity_negation + over.red()*opacity),
            round(base.green()*opacity_negation + over.green()*opacity),
            round(base.blue()*opacity_negation + over.blue()*opacity))
