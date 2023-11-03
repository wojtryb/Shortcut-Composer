import math

from api_krita import Krita
from composer_utils import Config
from composer_utils.label import LabelWidgetStyle
from .pie_config import PieConfig
from .pie_style import PieStyle


class StyleHolder:
    def __init__(self, pie_config: PieConfig) -> None:
        self._pie_config = pie_config
        self._base_size = Krita.screen_size/2560

        self.label_style = LabelWidgetStyle(
            icon_radius_callback=self._icon_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color)
        self.unscaled_label_style = LabelWidgetStyle(
            icon_radius_callback=self._unscaled_icon_radius,
            border_thickness_callback=self._border_thickness,
            active_color_callback=self._active_color,
            background_color_callback=self._background_color)
        self.pie_style = PieStyle(
            unscaled_label_style=self.unscaled_label_style,
            pie_radius_callback=self._pie_radius,
            deadzone_radius_callback=self._deadzone_radius,
            settings_button_radius_callback=self._settings_button_radius,
            accept_button_radius_callback=self._accept_button_radius)

    def _pie_radius(self):
        return round(
            165 * self._base_size
            * self._pie_config.PIE_RADIUS_SCALE.read()
            * Config.PIE_GLOBAL_SCALE.read())

    def _unscaled_icon_radius(self):
        return round(
            50 * self._base_size
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    def _icon_radius(self):
        elements = self._pie_config.ORDER.read()
        if not elements:
            max_radius = 1
        else:
            max_radius = round(
                self.pie_style.pie_radius * math.pi / len(elements))

        return min(self._unscaled_icon_radius(), max_radius)

    def _border_thickness(self):
        return round(self._unscaled_icon_radius()*0.05)

    def _deadzone_radius(self):
        elements = self._pie_config.ORDER.read()
        if not elements:
            return float("inf")
        return self.pie_style.accept_button_radius

    def _active_color(self):
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return self._pie_config.ACTIVE_COLOR.read()
        return Config.default_active_color

    def _background_color(self):
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return self._pie_config.BACKGROUND_COLOR.read()
        else:
            return Config.default_background_color

    def _accept_button_radius(self):
        return round(
            40 * self._base_size * Config.PIE_DEADZONE_GLOBAL_SCALE.read())

    def _settings_button_radius(self):
        return round(30 * self._base_size)
