
from typing import List

from data_components import Tag
from .pie_config import PieConfig, PresetPieConfig, EnumPieConfig
from .settings_gui import PieSettings, PresetPieSettings, EnumPieSettings
from .label import Label
from .pie_style import PieStyle
from .pie_config import PieConfig, EnumPieConfig, PresetPieConfig


def create_local_config(
    name: str,
    values: list,
    pie_radius_scale: float,
    icon_radius_scale: float,
) -> PieConfig:
    args = [name, values, pie_radius_scale, icon_radius_scale]
    if isinstance(values, Tag):
        return PresetPieConfig(*args)
    return EnumPieConfig(*args)

def create_pie_settings_window(
    values: List[Label],
    style: PieStyle,
    pie_config: PieConfig,
    parent=None
) -> PieSettings:
    if isinstance(pie_config, PresetPieConfig):
        return PresetPieSettings(values, style, pie_config, parent)
    elif isinstance(pie_config, EnumPieConfig):
        return EnumPieSettings(values, style, pie_config, parent)
    raise ValueError(f"Unknown pie config {pie_config}")