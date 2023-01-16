# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union, Any, Type, TypeVar, List
from enum import Enum

from api_krita import Krita
from api_krita.enums import Tool, BlendingMode

T = TypeVar('T', bound=Enum)


class Config(Enum):
    """
    Configuration fields available in the plugin.

    Each field remembers its default value:
    - `SHORT_VS_LONG_PRESS_TIME` = 0.3
    - `TRACKER_SENSITIVITY_SCALE` = 1.0
    - `TRACKER_DEADZONE` = 0
    - `FPS_LIMIT` = 60
    - `PIE_GLOBAL_SCALE` = 1.0
    - `PIE_ICON_GLOBAL_SCALE` = 1.0
    - `PIE_DEADZONE_GLOBAL_SCALE` = 1.0
    - `PIE_ANIMATION_TIME` = 0.2
    - `TAG_RED` = "★ My Favorites"
    - `TAG_GREEN` = "RGBA"
    - `TAG_BLUE` = "Erasers"
    - `BLENDING_MODES_VALUES` = ...
    - `MISC_TOOLS_VALUES` = ...
    - `SELECTION_TOOLS_VALUES` = ...
    - `TRANSFORM_MODES_VALUES` = ...


    Each field can:
    - return its default value
    - read current value from krita config file
    - write given value to krita config file

    Class holds a staticmethod which resets all config files.
    """

    SHORT_VS_LONG_PRESS_TIME = "Short vs long press time"
    TRACKER_SENSITIVITY_SCALE = "Tracker sensitivity scale"
    TRACKER_DEADZONE = "Tracker deadzone"
    FPS_LIMIT = "FPS limit"
    PIE_GLOBAL_SCALE = "Pie global scale"
    PIE_ICON_GLOBAL_SCALE = "Pie icon global scale"
    PIE_DEADZONE_GLOBAL_SCALE = "Pie deadzone global scale"
    PIE_ANIMATION_TIME = "pie animation time"

    TAG_RED = "Tag (red)"
    TAG_GREEN = "Tag (green)"
    TAG_BLUE = "Tag (blue)"

    BLENDING_MODES_VALUES = "Blending modes values"
    MISC_TOOLS_VALUES = "Misc tools values"
    SELECTION_TOOLS_VALUES = "Selection tools values"
    TRANSFORM_MODES_VALUES = "Transform modes values"

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
        """Write given value to krita config file."""
        Krita.write_setting(
            group="ShortcutComposer",
            name=self.value,
            value=value
        )

    def read_as_enums(self, enum: Type[T]) -> List[T]:
        value_string: str = self.read()
        values_list = value_string.split(";")
        return [enum[value] for value in values_list]

    @staticmethod
    def reset_defaults() -> None:
        """Reset all config files."""
        for field, default in _defaults.items():
            field.write(default)

    @staticmethod
    def get_sleep_time() -> int:
        """Read sleep time from FPS_LIMIT config field."""
        fps_limit = Config.FPS_LIMIT.read()
        return round(1000/fps_limit) if fps_limit else 1


def _format_enums(enums: List[Enum]):
    return ";".join([enum.name for enum in enums])


_defaults = {
    Config.SHORT_VS_LONG_PRESS_TIME: 0.3,
    Config.TRACKER_SENSITIVITY_SCALE: 1.0,
    Config.TRACKER_DEADZONE: 0,
    Config.FPS_LIMIT: 60,
    Config.PIE_GLOBAL_SCALE: 1.0,
    Config.PIE_ICON_GLOBAL_SCALE: 1.0,
    Config.PIE_DEADZONE_GLOBAL_SCALE: 1.0,
    Config.PIE_ANIMATION_TIME: 0.2,

    Config.TAG_RED: "★ My Favorites",
    Config.TAG_GREEN: "RGBA",
    Config.TAG_BLUE: "Erasers",

    Config.SELECTION_TOOLS_VALUES: _format_enums([
        Tool.FREEHAND_SELECTION,
        Tool.RECTANGULAR_SELECTION,
        Tool.CONTIGUOUS_SELECTION,
    ]),
    Config.MISC_TOOLS_VALUES: _format_enums([
        Tool.CROP,
        Tool.REFERENCE,
        Tool.GRADIENT,
        Tool.MULTI_BRUSH,
        Tool.ASSISTANTS,
    ]),
    Config.BLENDING_MODES_VALUES: _format_enums([
        BlendingMode.NORMAL,
        BlendingMode.OVERLAY,
        BlendingMode.COLOR,
        BlendingMode.MULTIPLY,
        BlendingMode.ADD,
        BlendingMode.SCREEN,
        BlendingMode.DARKEN,
        BlendingMode.LIGHTEN,
    ]),
    Config.TRANSFORM_MODES_VALUES: _format_enums([
        Tool.TRANSFORM_FREE,
        Tool.TRANSFORM_PERSPECTIVE,
        Tool.TRANSFORM_WARP,
        Tool.TRANSFORM_CAGE,
        Tool.TRANSFORM_LIQUIFY,
        Tool.TRANSFORM_MESH,
    ])
}
"""Maps default values to config fields."""
