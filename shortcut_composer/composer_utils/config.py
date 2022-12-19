from typing import Union, Any
from enum import Enum

from api_krita import Krita


class Config(Enum):
    """
    Configuration fields available in the plugin.

    Each field remembers its default value:
    - `SHORT_VS_LONG_PRESS_TIME` = 0.3
    - `SLIDER_SENSITIVITY_SCALE` = 1.0
    - `SLIDER_DEADZONE` = 0
    - `FPS_LIMIT` = 60
    - `PIE_GLOBAL_SCALE` = 1.0
    - `PIE_ICON_GLOBAL_SCALE` = 1.0
    - `PIE_DEADZONE_GLOBAL_SCALE` = 1.0
    - `TAG_RED` = "★ My Favorites"
    - `TAG_GREEN` = "RGBA"
    - `TAG_BLUE` = "Erasers"

    Each field can:
    - return its default value
    - read current value from krita config file
    - write given value to krita config file

    Class holds a staticmethod which resets all config files.
    """

    SHORT_VS_LONG_PRESS_TIME = "Short vs long press time"
    SLIDER_SENSITIVITY_SCALE = "Slider sensitivity scale"
    SLIDER_DEADZONE = "Slider deadzone"
    FPS_LIMIT = "FPS limit"
    PIE_GLOBAL_SCALE = "Pie global scale"
    PIE_ICON_GLOBAL_SCALE = "Pie icon global scale"
    PIE_DEADZONE_GLOBAL_SCALE = "Pie deadzone global scale"
    TAG_RED = "Tag (red)"
    TAG_GREEN = "Tag (green)"
    TAG_BLUE = "Tag (blue)"

    @property
    def default(self) -> Union[float, int]:
        """Return default value of the field."""
        return _defaults[self]

    def read(self) -> Any:
        """Read current value from krita config file."""
        return type(self.default)(Krita.read_setting(
            group="ShortcutComposer",
            name=self.value,
            default=str(self.default),
        ))

    def write(self, value: Any) -> None:
        "Write given value to krita config file."
        Krita.write_setting(
            group="ShortcutComposer",
            name=self.value,
            value=value
        )

    @staticmethod
    def reset_defaults():
        """Reset all config files."""
        for field, default in _defaults.items():
            field.write(default)

    @staticmethod
    def get_sleep_time():
        """Read sleep time from FPS_LIMIT config field."""
        fps_limit = Config.FPS_LIMIT.read()
        return 1/fps_limit if fps_limit else 0.001


_defaults = {
    Config.SHORT_VS_LONG_PRESS_TIME: 0.3,
    Config.SLIDER_SENSITIVITY_SCALE: 1.0,
    Config.SLIDER_DEADZONE: 0,
    Config.FPS_LIMIT: 60,
    Config.PIE_GLOBAL_SCALE: 1.0,
    Config.PIE_ICON_GLOBAL_SCALE: 1.0,
    Config.PIE_DEADZONE_GLOBAL_SCALE: 1.0,
    Config.TAG_RED: "★ My Favorites",
    Config.TAG_GREEN: "RGBA",
    Config.TAG_BLUE: "Erasers",
}
