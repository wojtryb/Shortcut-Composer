# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from PyQt5.QtGui import QColor

from api_krita import Krita
from api_krita.pyqt import RoundButton, Timer
from core_components import Instruction, InstructionHolder
from config_system import Field
from .action_values_window import ActionValuesWindow


class SettingsHandler:
    """
    Manages showing the MA settings window and button activating it.

    Creates settings window and button, and installs a instruction in
    multiple assignment action to show the button when the action key is
    pressed for a short time.

    Once clicked, the button shows the window in which the MA
    configuration can be modified.
    """

    def __init__(
        self,
        name: str,
        config: Field[list],
        instructions: InstructionHolder,
    ) -> None:
        to_cycle = config.read()
        if not to_cycle or not isinstance(to_cycle[0], Enum):
            return

        self._settings = ActionValuesWindow(type(to_cycle[0]), config)
        self._settings.setWindowTitle(f"Configure: {name}")

        self._button = RoundButton(
            radius_callback=lambda: 25,
            background_color_callback=lambda: QColor(75, 75, 75, 255),
            active_color_callback=lambda: QColor(100, 150, 230, 255),
            icon=Krita.get_icon("properties"),
            icon_scale=1.1,
            parent=None)
        self._button.clicked.connect(self._on_button_click)
        self._button.move(0, 0)
        self._button.hide()

        instructions.append(HandlerInstruction(self._settings, self._button))

    def _on_button_click(self) -> None:
        """Show the settings and hide the button after it was clicked."""
        self._settings.show()
        self._button.hide()


class HandlerInstruction(Instruction):
    """Instruction installed on the MA action which activates the button."""

    def __init__(self, settings: ActionValuesWindow, button: RoundButton):
        self._settings = settings
        self._button = button
        self._timer = Timer(self.timer_callback, 500)

    def on_key_press(self) -> None:
        """Start a timer which soon will run a callback once."""
        self._timer.start()

    def timer_callback(self) -> None:
        """Show a button in top left corner of painting area."""
        if not self._settings.isVisible():
            mdiArea = Krita.get_active_mdi_area()
            self._button.move(mdiArea.mapToGlobal(mdiArea.pos()))
            self._button.show()
        self._timer.stop()

    def on_every_key_release(self) -> None:
        """Hide the button when visible, or cancel the timer if not."""
        self._button.hide()
        self._timer.stop()
