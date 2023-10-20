import math

from composer_utils import LabelWidgetStyle, Config
from .pie_config import PieConfig
from .pie_style import PieStyle


class StyleManager:
    def __init__(self, pie_config: PieConfig) -> None:
        self.label_style = LabelWidgetStyle()
        self.pie_style = PieStyle(label_style=self.label_style)

        def pie_radius_callback() -> None:
            self.pie_style.pie_radius_scale \
                = pie_config.PIE_RADIUS_SCALE.read()
        pie_config.PIE_RADIUS_SCALE.register_callback(pie_radius_callback)
        pie_radius_callback()

        def icon_radius_callback() -> None:
            self.label_style.icon_radius_scale \
                = pie_config.ICON_RADIUS_SCALE.read()
        pie_config.ICON_RADIUS_SCALE.register_callback(icon_radius_callback)
        icon_radius_callback()

        def max_icon_radius_callback() -> None:
            elements = pie_config.ORDER.read()
            if not elements:
                self.label_style.max_icon_radius = 1
            else:
                self.label_style.max_icon_radius = round(
                    self.pie_style.pie_radius
                    * math.pi
                    / len(elements))
        pie_config.ORDER.register_callback(max_icon_radius_callback)
        max_icon_radius_callback()

        def deadzone_radius_callback() -> None:
            elements = pie_config.ORDER.read()
            if not elements:
                self.pie_style.deadzone_radius = float("inf")
            else:
                self.pie_style.deadzone_radius = \
                    self.pie_style.accept_button_radius
        pie_config.ORDER.register_callback(deadzone_radius_callback)
        deadzone_radius_callback()

        def active_color_callback() -> None:
            if pie_config.OVERRIDE_DEFAULT_THEME.read():
                self.label_style.active_color = pie_config.ACTIVE_COLOR.read()
            else:
                self.label_style.active_color = Config.default_active_color
        pie_config.ACTIVE_COLOR.register_callback(active_color_callback)
        active_color_callback()

        def bg_color_callback() -> None:
            if pie_config.OVERRIDE_DEFAULT_THEME.read():
                self.label_style.background_color = \
                    pie_config.BACKGROUND_COLOR.read()
            else:
                self.label_style.background_color = \
                    Config.default_background_color
        pie_config.BACKGROUND_COLOR.register_callback(bg_color_callback)
        bg_color_callback()
