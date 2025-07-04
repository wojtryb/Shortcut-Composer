# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

try:
    from PyQt5.QtGui import QColor
except ModuleNotFoundError:
    from PyQt6.QtGui import QColor

from api_krita import Krita
from composer_utils import Config
from composer_utils.label import LabelWidgetStyle
from .pie_config import PieConfig
from .pie_widget_utils import PieWidgetStyle


class PieStyleHolder:
    """
    Aggregates all visual information of the whole PieMenu action.

    It creates and holds style of PieWieget, labels in the PieSettings,
    as well as size of the buttons.

    Callbacks passed to those style objects are reading values from
    passed PieConfig. When user changes the configuration, GUI elements
    will read updated values.
    """

    def __init__(self, config: PieConfig) -> None:
        self._config = config
        self._base_size = Krita.screen_size/2560

        self.pie_widget_style = PieWidgetStyle(
            pie_radius_callback=self._pie_widget_radius,
            deadzone_radius_callback=self._deadzone_radius,
            background_opacity_callback=self._pie_widget_opacity,
            desired_icon_radius_callback=self._desired_pie_label_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color,
            max_lines_amount_callback=self._config.MAX_LINES_AMOUNT.read,
            max_signs_amount_callback=self._config.MAX_SIGNS_AMOUNT.read,
            abbreviation_sign_callback=self._abbreviation_sign_callback)
        """Style of the PieWidget."""

        self.settings_label_style = LabelWidgetStyle(
            icon_radius_callback=self._settings_label_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color,
            max_lines_amount_callback=lambda: 3,
            max_signs_amount_callback=lambda: 10,
            abbreviation_sign_callback=lambda: ".")
        """Style of labels in the PieSettings."""

        self.small_label_style = LabelWidgetStyle(
            icon_radius_callback=self._button_sized_label_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color,
            max_lines_amount_callback=lambda: 1,
            max_signs_amount_callback=lambda: 3,
            abbreviation_sign_callback=lambda: "")
        """Style of small label, the size of the settings button."""

    @property
    def accept_button_radius(self) -> int:
        """Radius of accept button which closes the pie in edit mode."""
        return round(
            40 * self._base_size * Config.PIE_DEADZONE_GLOBAL_SCALE.read())

    @property
    def settings_button_radius(self) -> int:
        """Radius of settings button which enters edit mode."""
        return round(
            30 * self._base_size
            * Config.PIE_GLOBAL_SCALE.read()
            * self._config.PIE_RADIUS_SCALE.read())

    def _pie_widget_radius(self) -> int:
        """Return radius of the PieWidget."""
        return round(
            165 * self._base_size
            * self._config.PIE_RADIUS_SCALE.read()
            * Config.PIE_GLOBAL_SCALE.read())

    def _settings_label_radius(self) -> int:
        """Return radius of LabelWidget in the PieSettings."""
        return round(
            50 * self._base_size
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    def _desired_pie_label_radius(self) -> int:
        """Return max radius of LabelWidget in the PieWidget"""
        return round(
            self._settings_label_radius()
            * self._config.ICON_RADIUS_SCALE.read())

    def _button_sized_label_radius(self) -> int:
        """Return radius of LabelWidget, the size of settings button."""
        return self.settings_button_radius + self._border_thickness()

    def _border_thickness(self) -> int:
        """Return border thickness of all LabelWidgets."""
        return round(self._settings_label_radius()*0.05)

    def _deadzone_radius(self) -> float:
        """Return deadzone radius of the PieWidget."""
        if not self.pie_widget_style.amount_of_labels:
            return float("inf")
        return self.accept_button_radius

    def _pie_widget_opacity(self) -> int:
        if self._config.OVERRIDE_DEFAULT_THEME.read():
            return self._config.PIE_OPACITY.read()
        return Config.DEFAULT_PIE_OPACITY.read()

    def _active_color(self) -> QColor:
        """Return active color of all Widgets (Pie and Label)."""
        if self._config.OVERRIDE_DEFAULT_THEME.read():
            return self._config.ACTIVE_COLOR.read()
        return Config.default_active_color

    def _background_color(self) -> QColor:
        """Return background color of all Widgets (Pie and Label)."""
        if self._config.OVERRIDE_DEFAULT_THEME.read():
            return self._config.BACKGROUND_COLOR.read()
        return Config.default_background_color

    def _abbreviation_sign_callback(self):
        """Return whether long text LabelWidgets should end with dot."""
        return "." if self._config.ABBREVIATE_WITH_DOT.read() else ""
