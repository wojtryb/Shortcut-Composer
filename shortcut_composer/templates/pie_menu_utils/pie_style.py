# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QColor

from composer_utils.label import LabelWidgetStyle


class PieStyle:

    def __init__(
        self,
        unscaled_label_style: LabelWidgetStyle,
        pie_radius_callback: Callable[[], int],
        deadzone_radius_callback: Callable[[], float],
        settings_button_radius_callback: Callable[[], int],
        accept_button_radius_callback: Callable[[], int],
    ) -> None:
        self._unscaled_label_style = unscaled_label_style

        self._pie_radius_callback = pie_radius_callback
        self._deadzone_radius_callback = deadzone_radius_callback
        self._settings_button_radius_callback = settings_button_radius_callback
        self._accept_button_radius_callback = accept_button_radius_callback

    @property
    def pie_radius(self) -> int:
        return self._pie_radius_callback()

    @property
    def deadzone_radius(self) -> float:
        return self._deadzone_radius_callback()

    @property
    def setting_button_radius(self) -> int:
        return self._settings_button_radius_callback()

    @property
    def accept_button_radius(self) -> int:
        return self._accept_button_radius_callback()

    @property
    def widget_radius(self) -> int:
        """Radius of the entire widget, including base and the icons."""
        return self.pie_radius + self._unscaled_label_style.icon_radius

    @property
    def border_thickness(self):
        """Thickness of border of the pie."""
        return self._unscaled_label_style.border_thickness

    @property
    def decorator_thickness(self):
        """Thickness of decorators near edges."""
        return self.border_thickness*4

    @property
    def area_thickness(self):
        """Thickness of the base area of pie menu."""
        return round(self.pie_radius*0.4)

    @property
    def inner_edge_radius(self):
        """Radius at which the base area starts."""
        return self.pie_radius - self.area_thickness

    @property
    def active_color(self) -> QColor:
        return self._unscaled_label_style.active_color

    @property
    def background_color(self) -> QColor:
        return self._unscaled_label_style.background_color

    @property
    def active_color_dark(self):
        """Color variation of active element."""
        return self._unscaled_label_style.active_color_dark

    @property
    def border_color(self):
        return self._unscaled_label_style.border_color

    @property
    def background_decorator_color(self):
        """Color of decorator near inner edge."""
        color = self.background_color
        color = QColor(color.red()-5, color.green()-5, color.blue()-5, 60)
        return color

    @property
    def pie_decorator_color(self):
        """Color of pie decorator near outer pie edge."""
        color = self.active_color_dark
        color = QColor(color.red()-5, color.green()-5, color.blue()-5, 60)
        return color
