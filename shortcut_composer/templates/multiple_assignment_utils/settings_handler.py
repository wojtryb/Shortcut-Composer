# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import List
from enum import Enum

from PyQt5.QtGui import QColor

from api_krita import Krita
from api_krita.pyqt import RoundButton
from core_components import Instruction
from config_system import Field
from .action_values_window import ActionValuesWindow


class SettingsHandler:
    def __init__(
        self,
        name: str,
        values: list,
        instructions: List[Instruction],
    ) -> None:
        self.values = Field(
            config_group=f"ShortcutComposer: {name}",
            name="Values",
            default=values)

        to_cycle = self.values.read()
        if not to_cycle or not isinstance(to_cycle[0], Enum):
            return

        self._settings = ActionValuesWindow(type(to_cycle[0]), self.values)

        self._settings_button = RoundButton(
            icon=Krita.get_icon("properties"),
            icon_scale=1.1,
            initial_radius=25,
            background_color=QColor(75, 75, 75, 255),
            active_color=QColor(100, 150, 230, 255))
        self._settings_button.clicked.connect(lambda: self._settings.show())
        self._settings_button.move(0, 0)
        self._settings_button.hide()

        instructions.append(HandlerInstruction(
            self._settings, self._settings_button))


@dataclass
class HandlerInstruction(Instruction):
    settings: ActionValuesWindow
    button: RoundButton

    def on_key_press(self) -> None:
        if not self.settings.isVisible():
            self.button.show()

    def on_every_key_release(self) -> None:
        self.button.hide()
