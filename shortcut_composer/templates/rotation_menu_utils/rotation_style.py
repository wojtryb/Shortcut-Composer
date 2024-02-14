# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QColor

from api_krita import Krita


class RotationStyle:

    def __init__(
        self,
        inner_zone_scale_callback: Callable[[], float],
        deadzone_scale_callback: Callable[[], float],
        active_color_callback: Callable[[], QColor],
        divisions_callback: Callable[[], int],
    ) -> None:

        self._inner_zone_scale_callback = inner_zone_scale_callback
        self._deadzone_scale_callback = deadzone_scale_callback
        self._active_color_callback = active_color_callback
        self._divisions_callback = divisions_callback

        self._base_size = Krita.screen_size/2560

    @property
    def deadzone_radius(self) -> int:
        return round(100 * self._deadzone_scale_callback() * self._base_size)

    @property
    def inner_zone_radius(self) -> int:
        free_zone = 75 * self._inner_zone_scale_callback() * self._base_size
        return round(self.deadzone_radius + free_zone)

    @property
    def transparent_border(self) -> int:
        return round(15 * self._base_size)

    @property
    def widget_radius(self) -> int:
        return round(self.inner_zone_radius + self.transparent_border)

    @property
    def active_color(self) -> QColor:
        return self._active_color_callback()

    @property
    def settings_button_radius(self) -> int:
        return round(30 * self._base_size)

    @property
    def discrete_pie_span(self) -> int:
        return 360//self._divisions_callback()
