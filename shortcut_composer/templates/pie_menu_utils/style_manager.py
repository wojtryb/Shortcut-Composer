import math

from api_krita import Krita
from composer_utils import Config
from composer_utils.label import LabelWidgetStyle
from .pie_config import PieConfig
from .pie_style import PieStyle


class StyleManager:
    def __init__(self, pie_config: PieConfig) -> None:
        self._pie_config = pie_config

        self.label_style = LabelWidgetStyle()
        self.unscaled_label_style = LabelWidgetStyle()
        self.pie_style = PieStyle(label_style=self.label_style)

        self._base_size = Krita.screen_size/2560

        self.pie_radius_callback()
        Config.PIE_GLOBAL_SCALE.register_callback(self.pie_radius_callback)
        pie_config.PIE_RADIUS_SCALE.register_callback(self.pie_radius_callback)

        self.icon_radius_callback()
        Config.PIE_GLOBAL_SCALE.register_callback(self.icon_radius_callback)
        pie_config.ORDER.register_callback(self.icon_radius_callback)
        pie_config.ICON_RADIUS_SCALE.register_callback(
            self.icon_radius_callback)

        self.deadzone_radius_callback()
        pie_config.ORDER.register_callback(self.deadzone_radius_callback)

        self.active_color_callback()
        pie_config.ACTIVE_COLOR.register_callback(self.active_color_callback)

        self.bg_color_callback()
        pie_config.BACKGROUND_COLOR.register_callback(self.bg_color_callback)

        self.accept_button_radius_callback()
        Config.PIE_DEADZONE_GLOBAL_SCALE.register_callback(
            self.accept_button_radius_callback)

        self.pie_style.setting_button_radius = round(30 * self._base_size)

    def pie_radius_callback(self) -> None:
        self.pie_style.pie_radius = round(
            165 * self._base_size
            * self._pie_config.PIE_RADIUS_SCALE.read()
            * Config.PIE_GLOBAL_SCALE.read())

    def icon_radius_callback(self) -> None:
        radius_scale = self._pie_config.ICON_RADIUS_SCALE.read()

        elements = self._pie_config.ORDER.read()
        if not elements:
            max_radius = 1
        else:
            max_radius = round(
                self.pie_style.pie_radius * math.pi / len(elements))

        unscaled_radius = round(
            50 * self._base_size * radius_scale
            * Config.PIE_ICON_GLOBAL_SCALE.read())

        self.label_style.icon_radius = min(unscaled_radius, max_radius)
        self.unscaled_label_style.icon_radius = unscaled_radius

        border_thickness = round(unscaled_radius*0.05)
        self.label_style.border_thickness = border_thickness
        self.unscaled_label_style.border_thickness = border_thickness

    def deadzone_radius_callback(self) -> None:
        elements = self._pie_config.ORDER.read()
        if not elements:
            self.pie_style.deadzone_radius = float("inf")
        else:
            self.pie_style.deadzone_radius = \
                self.pie_style.accept_button_radius

    def active_color_callback(self) -> None:
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            color = self._pie_config.ACTIVE_COLOR.read()
        else:
            color = Config.default_active_color

        self.label_style.active_color = color
        self.unscaled_label_style.active_color = color

    def bg_color_callback(self) -> None:
        if self._pie_config.OVERRIDE_DEFAULT_THEME.read():
            color = self._pie_config.BACKGROUND_COLOR.read()
        else:
            color = Config.default_background_color
        self.label_style.background_color = color

    def accept_button_radius_callback(self) -> None:
        self.pie_style.accept_button_radius = round(
            40 * self._base_size
            * Config.PIE_DEADZONE_GLOBAL_SCALE.read())
