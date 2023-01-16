# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita.pyqt import Painter
from ..pie_style import PieStyle
from ..label import Label


class PiePainter:

    def __init__(
        self,
        painter: Painter,
        labels: List[Label],
        style: PieStyle,
    ):
        self._painter = painter
        self._labels = labels
        self._style = style

        self._paint_deadzone_indicator()
        self._paint_base_wheel()
        self._paint_active_pie()
        self._paint_base_border()

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
            thickness=1,
        )
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.deadzone_radius-1,
            color=QColor(255, 128, 128, 120),
            thickness=1,
        )

    def _paint_base_wheel(self) -> None:
        """Paint a base circle and low opacity background to trick Windows."""
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.no_border_radius,
            color=QColor(128, 128, 128, 1),
        )
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.no_border_radius,
            color=self._style.background_color,
            thickness=self._style.area_thickness,
        )

    def _paint_base_border(self) -> None:
        """Paint a border on the inner edge of base circle."""
        self._painter.paint_wheel(
            center=self._center,
            outer_radius=self._style.inner_edge_radius,
            color=self._style.border_color,
            thickness=self._style.border_thickness,
        )

    def _paint_active_pie(self) -> None:
        """Paint a pie representing active label if there is one."""
        for label in self._labels:
            if not label.activation_progress.value:
                continue

            thickness_addition = round(
                0.15 * label.activation_progress.value
                * self._style.area_thickness)

            self._painter.paint_pie(
                center=self._center,
                outer_radius=self._style.no_border_radius + thickness_addition,
                angle=label.angle,
                span=360//len(self._labels),
                color=self._overlay_colors(
                    base=self._style.active_color_dark,
                    over=self._style.active_color,
                    opacity=label.activation_progress.value),
                thickness=self._style.area_thickness + thickness_addition,
            )

    @staticmethod
    def _overlay_colors(base: QColor, over: QColor, opacity: float):
        opacity_negation = 1-opacity
        return QColor(
            round(base.red()*opacity_negation + over.red()*opacity),
            round(base.green()*opacity_negation + over.green()*opacity),
            round(base.blue()*opacity_negation + over.blue()*opacity))
