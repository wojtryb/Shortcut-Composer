# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Type

from PyQt5.QtGui import QColor

from api_krita.enums.helpers import EnumGroup
from core_components import Controller, NumericController
from ..pie_settings import PieSettings
from .enum_group_pie_settings import EnumGroupPieSettings
from .numeric_pie_settings import NumericPieSettings
from .preset_pie_settings import PresetPieSettings


# TODO: or
def dispatch_pie_settings(controller: Controller) -> Type[PieSettings]:
    """Return the right settings type based on value type."""
    if isinstance(controller, NumericController):
        return NumericPieSettings
    elif issubclass(controller.TYPE, str):
        return PresetPieSettings
    elif issubclass(controller.TYPE, EnumGroup):
        return PresetPieSettings
    elif issubclass(controller.TYPE, QColor):
        return PieSettings
    raise ValueError(f"No known pie settings for type of `{controller.TYPE}`")
