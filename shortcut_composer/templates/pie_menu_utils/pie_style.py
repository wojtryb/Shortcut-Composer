# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QColor

from api_krita import Krita
from composer_utils.label import LabelWidgetStyle


class PieStyle:
    """
    Style which allows to paint a PieWidget.

    Callbacks passed in init determine base values. Rest of the values
    are calculated using those base values.
    """

    def __init__(
        self,
        label_style: LabelWidgetStyle
        = LabelWidgetStyle(),
        desired_icon_radius_callback: Callable[[], int]
        = lambda: round(Krita.screen_size*0.02),
        pie_radius_callback: Callable[[], int]
        = lambda: round(Krita.screen_size*0.065),
        deadzone_radius_callback: Callable[[], float]
        = lambda: round(Krita.screen_size*0.016),
        settings_button_radius_callback: Callable[[], int]
        = lambda: round(Krita.screen_size*0.012),
        accept_button_radius_callback: Callable[[], int]
        = lambda: round(Krita.screen_size*0.016),
        background_opacity_callback: Callable[[], int]
        = lambda: 75,
    ) -> None:
        self.label_style = label_style

        self._desired_icon_radius_callback = desired_icon_radius_callback
        self._pie_radius_callback = pie_radius_callback
        self._deadzone_radius_callback = deadzone_radius_callback
        self._settings_button_radius_callback = settings_button_radius_callback
        self._accept_button_radius_callback = accept_button_radius_callback
        self._background_opacity_callback = background_opacity_callback

        # Amount of labels in the pie that can be used by the callbacks
        # If it is used, user must guarantee that its value is correct
        # len(ORDER) should not be used, as pie register callbacks to it
        self.amount_of_labels = 0

    @property
    def pie_radius(self) -> int:
        """Radius of the pie, excluding the icons."""
        return self._pie_radius_callback()

    @property
    def deadzone_radius(self) -> float:
        """Radius of the deadzone in the center."""
        return self._deadzone_radius_callback()

    @property
    def setting_button_radius(self) -> int:
        """Radius of the button which activates settings widget."""
        return self._settings_button_radius_callback()

    @property
    def accept_button_radius(self) -> int:
        """Radius of the button which accepts the edit."""
        return self._accept_button_radius_callback()

    @property
    def widget_radius(self) -> int:
        """Radius of the entire widget, including base and the icons."""
        return self.pie_radius + self._desired_icon_radius_callback()

    @property
    def border_thickness(self) -> int:
        """Thickness of border of the pie."""
        return self.label_style.border_thickness

    @property
    def decorator_thickness(self) -> int:
        """Thickness of decorators near edges."""
        return self.border_thickness*4

    @property
    def area_thickness(self) -> int:
        """Thickness of the base area of pie menu."""
        return round(self.pie_radius*0.4)

    @property
    def inner_edge_radius(self) -> int:
        """Radius at which the base area starts."""
        return self.pie_radius - self.area_thickness

    @property
    def active_color(self) -> QColor:
        """Color of active elements."""
        return self.label_style.active_color

    @property
    def background_color(self) -> QColor:
        """Color of the widget background."""
        opaque = self.label_style.background_color
        return QColor(
            opaque.red(),
            opaque.green(),
            opaque.blue(),
            round(self._background_opacity_callback() * 255/100))

    @property
    def active_color_dark(self) -> QColor:
        """Color variation of active element."""
        return self.label_style.active_color_dark

    @property
    def border_color(self) -> QColor:
        """Color of the active pie border."""
        return self.label_style.border_color

    @property
    def background_decorator_color(self) -> QColor:
        """Color of decorator near inner edge."""
        color = self.label_style.background_color
        color = QColor(color.red()-5, color.green()-5, color.blue()-5, 60)
        return color

    @property
    def pie_decorator_color(self) -> QColor:
        """Color of pie decorator near outer pie edge."""
        color = self.active_color_dark
        color = QColor(color.red()-5, color.green()-5, color.blue()-5, 60)
        return color
