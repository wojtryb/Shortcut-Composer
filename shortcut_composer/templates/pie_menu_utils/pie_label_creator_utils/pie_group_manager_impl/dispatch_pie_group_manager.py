# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from ..pie_group_manager import PieGroupManager
from .enum_pie_group_manager import EnumPieGroupManager
from .preset_pie_group_manager import PresetPieGroupManager
from .invalid_pie_group_manager import InvalidPieGroupManager


def dispatch_group_manager(value_type: type) -> PieGroupManager:
    """Return group manager correct for provided type"""
    if issubclass(value_type, str):
        return PresetPieGroupManager()
    elif issubclass(value_type, EnumGroup):
        return EnumPieGroupManager(value_type)
    return InvalidPieGroupManager()
