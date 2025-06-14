# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QColor

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from .group_manager import GroupManager
from .enum_group_manager import EnumGroupManager
from .preset_group_manager import PresetGroupManager


def dispatch_group_manager(controller: Controller) -> GroupManager:
    if issubclass(controller.TYPE, str):
        return PresetGroupManager()
    elif issubclass(controller.TYPE, EnumGroup):
        return EnumGroupManager(controller)
    # HACK: so far GroupManager is not needed for QColor, but it must be given
    elif issubclass(controller.TYPE, QColor):
        return EnumGroupManager(controller)
    raise ValueError(f"No known GroupManager for type of `{controller.TYPE}`")
