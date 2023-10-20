# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Type
from enum import Enum

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from ..pie_settings import PieSettings
from .enum_group_pie_settings import EnumGroupPieSettings
from .numeric_pie_settings import NumericPieSettings
from .preset_pie_settings import PresetPieSettings
from .enum_pie_settings import EnumPieSettings


def dispatch_pie_settings(controller: Controller) -> Type[PieSettings]:
    """Return the right settings type based on value type."""
    if issubclass(controller.TYPE, str):
        return PresetPieSettings
    elif issubclass(controller.TYPE, int):
        return NumericPieSettings
    elif issubclass(controller.TYPE, EnumGroup):
        return EnumGroupPieSettings
    elif issubclass(controller.TYPE, Enum):
        return EnumPieSettings
    raise ValueError(f"No known pie settings for type of `{controller.TYPE}`")
