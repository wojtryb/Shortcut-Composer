# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from ..pie_group_manager import PieGroupManager
from .enum_pie_group_manager import EnumPieGroupManager
from .preset_pie_group_manager import PresetPieGroupManager
from .invalid_pie_group_manager import InvalidPieGroupManager


def dispatch_pie_group_manager(controller: Controller) -> PieGroupManager:
    if issubclass(controller.TYPE, str):
        return PresetPieGroupManager()
    elif issubclass(controller.TYPE, EnumGroup):
        return EnumPieGroupManager(controller)
    return InvalidPieGroupManager(controller.TYPE)
