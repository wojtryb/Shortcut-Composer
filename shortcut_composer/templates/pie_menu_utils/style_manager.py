import math

from api_krita import Krita
from composer_utils import Config
from composer_utils.label import LabelWidgetStyle
from .pie_config import PieConfig
from .pie_style import PieStyle


class StyleManager:
    def __init__(self, pie_config: PieConfig) -> None:
        self._pie_config = pie_config
        self._base_size = Krita.screen_size/2560

        self.label_style = LabelWidgetStyle(
            icon_radius_callback=self.icon_radius_callback,
            border_thickness_callback=self.border_thickness_callback,
            active_color_callback=self.active_color_callback,
            background_color_callback=self.bg_color_callback)
        self.unscaled_label_style = LabelWidgetStyle(
            icon_radius_callback=self.unscaled_icon_radius_callback,
            border_thickness_callback=self.border_thickness_callback,
            active_color_callback=self.active_color_callback,
            background_color_callback=self.bg_color_callback)
        self.pie_style = PieStyle(
            label_style=self.label_style,
            unscaled_label_style=self.unscaled_label_style,
            pie_radius_callback=self.pie_radius_callback,
            deadzone_radius_callback=self.deadzone_radius_callback,
            settings_button_radius_callback=self.settings_button_radius_callback,
            accept_button_radius_callback=self.accept_button_radius_callback)

    def pie_radius_callback(self):
        return round(
            165 * self._base_size
            * self._pie_config.PIE_RADIUS_SCALE.read()
            * Config.PIE_GLOBAL_SCALE.read())

    def unscaled_icon_radius_callback(self):
        return round(
            50 * self._base_size
            * self._pie_config.ICON_RADIUS_SCALE.read()
            * Config.PIE_ICON_GLOBAL_SCALE.read())

    def icon_radius_callback(self):
        elements = self._pie_config.ORDER.read()
        if not elements:
            max_radius = 1
        else:
            max_radius = round(
                self.pie_style.pie_radius * math.pi / len(elements))

        return min(self.unscaled_icon_radius_callback(), max_radius)

    def border_thickness_callback(self):
        return round(self.unscaled_icon_radius_callback()*0.05)

    def deadzone_radius_callback(self):
        elements = self._pie_config.ORDER.read()
        if not elements:
            return float("inf")
        return self.pie_style.accept_button_radius

    def active_color_callback(self):
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return self._pie_config.ACTIVE_COLOR.read()
        return Config.default_active_color

    def bg_color_callback(self):
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            return self._pie_config.BACKGROUND_COLOR.read()
        else:
            return Config.default_background_color

    def accept_button_radius_callback(self):
        return round(
            40 * self._base_size * Config.PIE_DEADZONE_GLOBAL_SCALE.read())

    def settings_button_radius_callback(self):
        return round(30 * self._base_size)
