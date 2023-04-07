
from typing import List, TypeVar

from data_components import Tag
from .pie_config import PieConfig, PresetPieConfig, EnumPieConfig
from .settings_gui import PieSettings, PresetPieSettings, EnumPieSettings
from .label import Label
from .pie_style import PieStyle

T = TypeVar("T")


def create_local_config(
    name: str,
    values: List[T],
    pie_radius_scale: float,
    icon_radius_scale: float,
) -> PieConfig[T]:
    config_name = f"ShortcutComposer: {name}"
    args = [config_name, values, pie_radius_scale, icon_radius_scale]
    if isinstance(values, Tag):
        return PresetPieConfig(*args)
    return EnumPieConfig(*args)


def create_pie_settings_window(
    values: List[Label],
    used_values: List[Label],
    style: PieStyle,
    pie_config: PieConfig,
    parent=None
) -> PieSettings:
    args = [values, used_values, style, pie_config, parent]
    if isinstance(pie_config, PresetPieConfig):
        return PresetPieSettings(*args)
    elif isinstance(pie_config, EnumPieConfig):
        return EnumPieSettings(*args)
    raise ValueError(f"Unknown pie config {pie_config}")
