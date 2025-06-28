# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QColor

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from ..pie_label_creator import PieLabelCreator
from .enum_pie_label_creator import EnumPieLabelCreator
from .preset_pie_label_creator import PresetPieLabelCreator


def dispatch_pie_label_creator(controller: Controller) -> PieLabelCreator:
    if issubclass(controller.TYPE, str):
        return PresetPieLabelCreator()
    elif issubclass(controller.TYPE, EnumGroup):
        return EnumPieLabelCreator(controller)
    # HACK: so far GroupManager is not needed for QColor, but it must be given
    elif issubclass(controller.TYPE, QColor):
        return EnumPieLabelCreator(controller)
    raise ValueError(f"No known PieValueManager for type of {controller.TYPE}")
