# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, TypeVar, Optional
from enum import Enum

from PyQt5.QtGui import QColor

from core_components import Controller
from data_components import Tag
from .pie_config import PieConfig, PresetPieConfig, NonPresetPieConfig
from .settings_gui import (
    PieSettings,
    PresetPieSettings,
    EnumPieSettings,
    NumericPieSettings)
from .pie_style import PieStyle

T = TypeVar("T")


def create_local_config(
    name: str,
    values: List[T],
    controller_type: type,
    pie_radius_scale: float,
    icon_radius_scale: float,
    save_local: bool,
    background_color: Optional[QColor],
    active_color: QColor,
) -> PieConfig[T]:
    """Create and return the right local config based on labels type."""
    config_name = f"ShortcutComposer: {name}"
    args = [config_name, values, pie_radius_scale, icon_radius_scale,
            save_local, background_color, active_color]

    if issubclass(controller_type, str):
        is_tag_mode = isinstance(values, Tag)
        return PresetPieConfig(*args, is_tag_mode)  # type: ignore
    return NonPresetPieConfig(*args)


def create_pie_settings_window(
    controller: Controller,
    style: PieStyle,
    pie_config: PieConfig,
    parent=None
) -> PieSettings:
    """Create and return the right settings based on labels type."""
    args = [pie_config, style, parent]

    if issubclass(controller.TYPE, str):
        return PresetPieSettings(*args)
    elif issubclass(controller.TYPE, Enum):
        return EnumPieSettings(controller, *args)
    elif issubclass(controller.TYPE, float):
        return NumericPieSettings(*args)
    raise ValueError(f"Unknown pie config {pie_config}")
