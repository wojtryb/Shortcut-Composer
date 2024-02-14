# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QColor


class RotationStyle:

    def __init__(
        self,
        widget_radius_callback: Callable[[], int],
        deadzone_radius_callback: Callable[[], int],
        active_color_callback: Callable[[], QColor],
        settings_button_radius_callback: Callable[[], int],
        divisions_callback: Callable[[], int],
    ) -> None:

        self._widget_radius_callback = widget_radius_callback
        self._deadzone_radius_callback = deadzone_radius_callback
        self._active_color_callback = active_color_callback
        self._settings_button_radius_callback = settings_button_radius_callback
        self._divisions_callback = divisions_callback

    @property
    def deadzone_radius(self) -> int:
        return self._deadzone_radius_callback()

    @property
    def widget_radius(self) -> int:
        return self._widget_radius_callback()

    @property
    def active_color(self) -> QColor:
        return self._active_color_callback()

    @property
    def settings_button_radius(self) -> int:
        return self._settings_button_radius_callback()

    @property
    def divisions(self) -> int:
        return self._divisions_callback()
