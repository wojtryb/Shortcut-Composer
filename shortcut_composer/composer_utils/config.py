from typing import Union, Any
from enum import Enum

from .krita_setting import read_setting


class Config(Enum):
    SHORT_VS_LONG_PRESS_TIME = "Short vs long press time"
    PIXELS_IN_UNIT = "Pixels in unit"
    SLIDER_DEADZONE = "Slider deadzone"
    FPS_LIMIT = "FPS limit"
    PIE_GLOBAL_SCALE = "Pie global scale"
    PIE_ICON_GLOBAL_SCALE = "Pie icon global scale"
    PIE_DEADZONE_GLOBAL_SCALE = "Pie deadzone global scale"

    @property
    def default(self) -> Union[float, int]:
        return _defaults[self]

    def get(self) -> Any:
        return type(self.default)(read_setting(self.value, str(self.default)))


_defaults = {
    Config.SHORT_VS_LONG_PRESS_TIME: 0.3,
    Config.PIXELS_IN_UNIT: 50,
    Config.SLIDER_DEADZONE: 0,
    Config.FPS_LIMIT: 60,
    Config.PIE_GLOBAL_SCALE: 1.0,
    Config.PIE_ICON_GLOBAL_SCALE: 1.0,
    Config.PIE_DEADZONE_GLOBAL_SCALE: 1.0,
}
