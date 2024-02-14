from api_krita import Krita
from .rotation_config import RotationConfig
from .rotation_style import RotationStyle


class RotationStyleHolder:
    def __init__(self, config: RotationConfig) -> None:
        self._config = config
        self._base_size = Krita.screen_size/2560

        self.rotation_style = RotationStyle(
            widget_radius_callback=self._widget_radius,
            deadzone_radius_callback=self._deadzone_radius,
            settings_button_radius_callback=self._settings_button_radius,
            active_color_callback=self._config.ACTIVE_COLOR.read,
            divisions_callback=self._config.DIVISIONS.read)

    def _widget_radius(self) -> int:
        free_zone = 75 * self._config.INNER_ZONE_SCALE.read() * self._base_size
        return round(self._deadzone_radius() + free_zone)

    def _deadzone_radius(self) -> int:
        radius = 100 * self._config.DEADZONE_SCALE.read() * self._base_size
        return round(radius)

    def _settings_button_radius(self):
        return round(30 * self._base_size)
