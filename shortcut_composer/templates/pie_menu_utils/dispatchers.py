
from typing import List, TypeVar, Optional
from enum import Enum

from PyQt5.QtGui import QColor

from data_components import Tag
from .pie_config import PieConfig, PresetPieConfig, NonPresetPieConfig
from .settings_gui import (
    PieSettings,
    PresetPieSettings,
    EnumPieSettings,
    NumericPieSettings,
)
from .label import Label
from .pie_style import PieStyle

T = TypeVar("T")


def create_local_config(
    name: str,
    values: List[T],
    pie_radius_scale: float,
    icon_radius_scale: float,
    background_color: Optional[QColor],
    active_color: QColor,
) -> PieConfig[T]:
    """Create and return the right local config based on values type."""
    config_name = f"ShortcutComposer: {name}"
    args = [config_name, values, pie_radius_scale, icon_radius_scale,
            background_color, active_color]
    if isinstance(values, Tag):
        return PresetPieConfig(*args)  # type: ignore
    return NonPresetPieConfig(*args)


def create_pie_settings_window(
    values: List[Label],
    used_values: List[Label],
    style: PieStyle,
    pie_config: PieConfig,
    parent=None
) -> PieSettings:
    """Create and return the right settings based on config and value type."""
    args = [pie_config, style, parent]
    if isinstance(pie_config, PresetPieConfig):
        return PresetPieSettings(*args)
    elif isinstance(pie_config, NonPresetPieConfig):
        if not values or isinstance(values[0], Enum):
            return NumericPieSettings(*args)
        return EnumPieSettings(values, used_values, *args)
    raise ValueError(f"Unknown pie config {pie_config}")
