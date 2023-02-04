# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union, Any, TypeVar, List
from enum import Enum

from api_krita import Krita
from api_krita.enums import Tool, BlendingMode, TransformMode

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
    - `TAG_RED_VALUES` = ...
    - `TAG_GREEN_VALUES` = ...
    - `TAG_BLUE_VALUES` = ...
    - `BLENDING_MODES_VALUES` = ...
    - `MISC_TOOLS_VALUES` = ...
    - `SELECTION_TOOLS_VALUES` = ...
    - `TRANSFORM_MODES_VALUES` = ...
    - `CREATE_BLENDING_LAYER_VALUES` = ...

    Each field can:
    - return its default value
    - read current value from krita config file in correct type
    - write given value to krita config file

    Class holds a staticmethod which resets all config files.

    VALUES configs are string representations of lists. They hold values
    to use in given action with elements separated with tabulators.
    These are needed to be further parsed using TagConfigValues or
    EnumConfigValues.
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

    TAG_RED_VALUES = "Tag (red) values"
    TAG_GREEN_VALUES = "Tag (green) values"
    TAG_BLUE_VALUES = "Tag (blue) values"

    BLENDING_MODES_VALUES = "Blending modes values"
    MISC_TOOLS_VALUES = "Misc tools values"
    SELECTION_TOOLS_VALUES = "Selection tools values"
    TRANSFORM_MODES_VALUES = "Transform modes values"
    CREATE_BLENDING_LAYER_VALUES = "Create blending layer values"

    @property
    def default(self) -> Union[float, int, str]:
        """Return default value of the field."""
        return _defaults[self]

    def read(self) -> Any:
        """Read current value from krita config file."""
        setting = Krita.read_setting(
            group="ShortcutComposer",
            name=self.value,
            default=str(self.default),
        )
        try:
            return type(self.default)(setting)
        except ValueError:
            print(f"Can't parse {setting} to {type(self.default)}")
            return self.default

    def write(self, value: Any) -> None:
        """Write given value to krita config file."""
        Krita.write_setting(
            group="ShortcutComposer",
            name=self.value,
            value=value
        )

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

    @staticmethod
    def format_enums(enums: List[Enum]) -> str:
        return "\t".join([enum.name for enum in enums])


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

    Config.TAG_RED_VALUES: "",
    Config.TAG_GREEN_VALUES: "",
    Config.TAG_BLUE_VALUES: "",

    Config.SELECTION_TOOLS_VALUES: Config.format_enums([
        Tool.FREEHAND_SELECTION,
        Tool.RECTANGULAR_SELECTION,
        Tool.CONTIGUOUS_SELECTION,
    ]),
    Config.MISC_TOOLS_VALUES: Config.format_enums([
        Tool.CROP,
        Tool.REFERENCE,
        Tool.GRADIENT,
        Tool.MULTI_BRUSH,
        Tool.ASSISTANTS,
    ]),
    Config.BLENDING_MODES_VALUES: Config.format_enums([
        BlendingMode.NORMAL,
        BlendingMode.OVERLAY,
        BlendingMode.COLOR,
        BlendingMode.MULTIPLY,
        BlendingMode.ADD,
        BlendingMode.SCREEN,
        BlendingMode.DARKEN,
        BlendingMode.LIGHTEN,
    ]),
    Config.CREATE_BLENDING_LAYER_VALUES: Config.format_enums([
        BlendingMode.NORMAL,
        BlendingMode.ERASE,
        BlendingMode.OVERLAY,
        BlendingMode.COLOR,
        BlendingMode.MULTIPLY,
        BlendingMode.ADD,
        BlendingMode.SCREEN,
        BlendingMode.DARKEN,
        BlendingMode.LIGHTEN,
    ]),
    Config.TRANSFORM_MODES_VALUES: Config.format_enums([
        TransformMode.FREE,
        TransformMode.PERSPECTIVE,
        TransformMode.WARP,
        TransformMode.CAGE,
        TransformMode.LIQUIFY,
        TransformMode.MESH,
    ])
}
"""Maps default values to config fields."""
