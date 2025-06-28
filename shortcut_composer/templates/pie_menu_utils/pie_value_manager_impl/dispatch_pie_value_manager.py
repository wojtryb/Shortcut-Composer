# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QColor

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from ..pie_value_manager import PieValueManager
from .enum_group_manager import EnumPieValueManager
from .preset_group_manager import PresetPieValueManager


def dispatch_pie_value_manager(controller: Controller) -> PieValueManager:
    if issubclass(controller.TYPE, str):
        return PresetPieValueManager()
    elif issubclass(controller.TYPE, EnumGroup):
        return EnumPieValueManager(controller)
    # HACK: so far GroupManager is not needed for QColor, but it must be given
    elif issubclass(controller.TYPE, QColor):
        return EnumPieValueManager(controller)
    raise ValueError(f"No known PieValueManager for type of {controller.TYPE}")
