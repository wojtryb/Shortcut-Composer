# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List
from dataclasses import dataclass

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita.pyqt import Painter
from ..pie_style import PieStyle
from ..label import Label


@dataclass
class PiePainter:
    """Uses provided painter and parts of widget data to paint it."""

    painter: Painter
    labels: List[Label]
    style: PieStyle
    edit_mode: bool

    def __post_init__(self):
        """Paint the widget which created the passed painter."""
        self._paint_deadzone_indicator()
        self._paint_base_wheel()
        self._paint_active_pie()
        self._paint_base_border()

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self.style.widget_radius, self.style.widget_radius)

    def _paint_deadzone_indicator(self) -> None:
        """Paint the circle representing deadzone, when its valid."""
        if self.style.deadzone_radius == float("inf"):
            return

        self.painter.paint_wheel(
            center=self._center,
            outer_radius=self.style.deadzone_radius,
            color=QColor(128, 255, 128, 120),
            thickness=1,
        )
        self.painter.paint_wheel(
            center=self._center,
            outer_radius=self.style.deadzone_radius-1,
            color=QColor(255, 128, 128, 120),
            thickness=1,
        )

    def _paint_base_wheel(self) -> None:
        """Paint a base circle and low opacity background to trick Windows."""
        self.painter.paint_wheel(
            center=self._center,
            outer_radius=self.style.no_border_radius,
            color=QColor(128, 128, 128, 1),
        )
        self.painter.paint_wheel(
            center=self._center,
            outer_radius=self.style.no_border_radius,
            color=self.style.background_color,
            thickness=self.style.area_thickness,
        )

    def _paint_base_border(self) -> None:
        """Paint a border on the inner edge of base circle."""
        self.painter.paint_wheel(
            center=self._center,
            outer_radius=self.style.inner_edge_radius,
            color=self.style.border_color,
            thickness=self.style.border_thickness,
        )

    def _paint_active_pie(self) -> None:
        """Paint a pie representing active label if there is one."""
        for label in self.labels:
            if not label.activation_progress.value:
                continue

            thickness_addition = round(
                0.15 * label.activation_progress.value
                * self.style.area_thickness)

            self.painter.paint_pie(
                center=self._center,
                outer_radius=self.style.no_border_radius + thickness_addition,
                angle=label.angle,
                span=360//len(self.labels),
                color=self._pick_pie_color(label),
                thickness=self.style.area_thickness + thickness_addition,
            )

    def _pick_pie_color(self, label: Label) -> QColor:
        """Pick color of pie based on widget mode and animation progress."""
        if not self.edit_mode:
            return self._overlay_colors(
                self.style.active_color_dark,
                self.style.active_color,
                opacity=label.activation_progress.value)
        return self._overlay_colors(
            self.style.icon_color,
            self.style.border_color,
            opacity=label.activation_progress.value)

    @staticmethod
    def _overlay_colors(base: QColor, over: QColor, opacity: float) -> QColor:
        opacity_negation = 1-opacity
        return QColor(
            round(base.red()*opacity_negation + over.red()*opacity),
            round(base.green()*opacity_negation + over.green()*opacity),
            round(base.blue()*opacity_negation + over.blue()*opacity))
