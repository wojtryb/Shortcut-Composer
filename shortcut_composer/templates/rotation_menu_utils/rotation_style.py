# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QColor

from api_krita import Krita


class RotationStyle:
    """
    Style which allows to paint a RotationWidget.

    Callbacks passed in init determine base values. Rest of the values
    is calculated using those base values.
    """

    def __init__(
        self,
        deadzone_scale_callback: Callable[[], float],
        inner_zone_scale_callback: Callable[[], float],
        divisions_callback: Callable[[], int],
        active_color_callback: Callable[[], QColor],
        outline_opacity_callback: Callable[[], int],
    ) -> None:

        self._deadzone_scale_callback = deadzone_scale_callback
        self._inner_zone_scale_callback = inner_zone_scale_callback
        self._divisions_callback = divisions_callback
        self._active_color_callback = active_color_callback
        self._outline_opacity_callback = outline_opacity_callback

        self._base_size = Krita.screen_size/2560

    @property
    def deadzone_radius(self) -> int:
        """Radius of the deadzone in the center."""
        return round(100 * self._deadzone_scale_callback() * self._base_size)

    @property
    def inner_zone_span(self) -> int:
        """Length of the zone after the deadzone, excluding it."""
        return round(75 * self._inner_zone_scale_callback() * self._base_size)

    @property
    def inner_zone_radius(self) -> int:
        """Radius of the zone after the deadzone, including it."""
        return round(self.deadzone_radius + self.inner_zone_span)

    @property
    def transparent_border(self) -> int:
        """Length of the zone after inner zone required by animations."""
        return round(15 * self._base_size)

    @property
    def decorator_thickness(self) -> int:
        """Thickness of decorator in the selection pie."""
        return self.inner_zone_span//4

    @property
    def border_thickness(self) -> int:
        """Thickness of border of the selection pie."""
        return round(2 * self._base_size)

    @property
    def widget_radius(self) -> int:
        """Radius of the entire widget."""
        return round(self.inner_zone_radius + self.transparent_border)

    @property
    def active_color(self) -> QColor:
        """Color of the selection pie."""
        return self._active_color_callback()

    @property
    def active_color_dark(self) -> QColor:
        """Color variation of selection pie decorator."""
        return QColor(
            round(self.active_color.red()*0.92),
            round(self.active_color.green()*0.92),
            round(self.active_color.blue()*0.92))

    @property
    def border_color(self) -> QColor:
        """Color of selection pie border."""
        return QColor(
            min(round(self.active_color.red()*0.7), 255),
            min(round(self.active_color.green()*0.7), 255),
            min(round(self.active_color.blue()*0.7), 255))

    @property
    def settings_button_radius(self) -> int:
        """Radius of the button which activates settings widget."""
        return round(30 * self._base_size)

    @property
    def intervallic_pie_span(self) -> int:
        """Span of the pie in the intervallic zone."""
        return 360//self._divisions_callback()

    @property
    def precise_pie_span(self) -> int:
        """Span of the pie in the precise zone."""
        return 10

    @property
    def outline_opacity(self) -> int:
        """Opacity [0-255] of the outline for deadzone, and inner zone."""
        opacity = round(self._outline_opacity_callback() * 255/100)
        return sorted([0, opacity, 255])[1]
