# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QColor

from composer_utils.label import LabelWidgetStyle


class PieStyle:
    """
    Holds and calculates configuration of displayed elements.

    Style elements are calculated based on passed local config and
    imported global config.

    They are also affected by length of passed items list which size can
    change over time.
    """

    def __init__(self, label_style: LabelWidgetStyle) -> None:
        self.label_style = label_style

        self.pie_radius = 400
        self.deadzone_radius = 100.0
        self.setting_button_radius = 50
        self.accept_button_radius = 50

    @property
    def widget_radius(self) -> int:
        """Radius of the entire widget, including base and the icons."""
        return self.pie_radius + self.label_style.icon_radius

    @property
    def border_thickness(self):
        """Thickness of border of the pie."""
        return self.label_style.border_thickness

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
        return self.label_style.active_color

    @property
    def background_color(self) -> QColor:
        return self.label_style.background_color

    @property
    def active_color_dark(self):
        """Color variation of active element."""
        return self.label_style.active_color_dark

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
