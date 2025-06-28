# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QColor

from api_krita import Krita
from composer_utils import Config
from composer_utils.label import LabelWidgetStyle
from .pie_config import PieConfig
from .pie_widget_utils import PieWidgetStyle


class PieStyleHolder:
    """Creates and gives access to style objects based on passed config."""

    def __init__(self, pie_config: PieConfig) -> None:
        self._pie_config = pie_config
        self._base_size = Krita.screen_size/2560

        self.pie_style = PieWidgetStyle(
            pie_radius_callback=self._pie_radius,
            deadzone_radius_callback=self._deadzone_radius,
            background_opacity_callback=self._pie_config.PIE_OPACITY.read,
            desired_icon_radius_callback=self._desired_icon_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color,
            max_lines_amount_callback=self._pie_config.MAX_LINES_AMOUNT.read,
            max_signs_amount_callback=self._pie_config.MAX_SIGNS_AMOUNT.read,
            abbreviation_sign_callback=self._abbreviation_sign_callback)
        """Style of the pie widget."""

        self.settings_label_style = LabelWidgetStyle(
            icon_radius_callback=self._unscaled_icon_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color,
            max_lines_amount_callback=lambda: 3,
            max_signs_amount_callback=lambda: 10,
            abbreviation_sign_callback=lambda: ".")
        """Style of labels in the settings."""

        self.small_label_style = LabelWidgetStyle(
            icon_radius_callback=self._button_sized_icon_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color,
            max_lines_amount_callback=lambda: 1,
            max_signs_amount_callback=lambda: 3,
            abbreviation_sign_callback=lambda: "")
        """Style of label, being the size of button activating settings."""

    @property
    def accept_button_radius(self) -> int:
        """Return radius of accept button based on configured value."""
        return round(
            40 * self._base_size * Config.PIE_DEADZONE_GLOBAL_SCALE.read())

    @property
    def settings_button_radius(self) -> int:
        """Return radius of settings button based on configured value."""
        return round(
            30 * self._base_size
            * Config.PIE_GLOBAL_SCALE.read()
            * self._pie_config.PIE_RADIUS_SCALE.read())

    def _pie_radius(self) -> int:
        """Return pie radius based on configured value."""
        return round(
            165 * self._base_size
            * self._pie_config.PIE_RADIUS_SCALE.read()
            * Config.PIE_GLOBAL_SCALE.read())

    def _unscaled_icon_radius(self) -> int:
        """Return unscaled icon radius based on configured value."""
        return round(
            50 * self._base_size
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    def _desired_icon_radius(self) -> int:
        return round(
            self._unscaled_icon_radius()
            * self._pie_config.ICON_RADIUS_SCALE.read())

    def _button_sized_icon_radius(self) -> int:
        """Return icon radius that is visually the same as settings button."""
        return self.settings_button_radius + self._border_thickness()

    def _border_thickness(self) -> int:
        """Return border thickness based on configured value."""
        return round(self._unscaled_icon_radius()*0.05)

    def _deadzone_radius(self) -> float:
        """Return deadzone radius based on configured value."""
        if not self.pie_style.amount_of_labels:
            return float("inf")
        return self.accept_button_radius

    def _active_color(self) -> QColor:
        """Return active color based on configured value."""
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return self._pie_config.ACTIVE_COLOR.read()
        return Config.default_active_color

    def _background_color(self) -> QColor:
        """Return background color based on configured value."""
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return self._pie_config.BACKGROUND_COLOR.read()
        return Config.default_background_color

    def _abbreviation_sign_callback(self):
        return "." if self._pie_config.ABBREVIATE_WITH_DOT.read() else ""
