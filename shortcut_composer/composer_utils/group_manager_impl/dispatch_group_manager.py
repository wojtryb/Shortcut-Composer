# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from ..group_manager import GroupManager
from .enum_pie_group_manager import EnumGroupManager
from .preset_pie_group_manager import PresetGroupManager
from .invalid_pie_group_manager import InvalidGroupManager


def dispatch_group_manager(value_type: type) -> GroupManager:
    """Return group manager correct for provided type"""
    if issubclass(value_type, str):
        return PresetGroupManager()
    elif issubclass(value_type, EnumGroup):
        return EnumGroupManager(value_type)
    return InvalidGroupManager()
