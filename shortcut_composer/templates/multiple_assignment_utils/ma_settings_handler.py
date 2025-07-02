# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cached_property

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget

from api_krita import Krita
from api_krita.pyqt import RoundButton, Timer
from core_components import Controller, Instruction
from .ma_settings import MaSettings
from .ma_config import MaConfig


class MaSettingsHandler(Instruction):
    """
    Manages showing the MaSettings and button activating it.

    Creates settings window and button, and installs an instruction in
    MultipleAssignment action to show the button when the action key is
    pressed for a short time.

    Once clicked, the button shows the window in which the MA
    configuration can be modified.
    """

    def __init__(
        self,
        name: str,
        controller: Controller,
        config: MaConfig,
    ) -> None:
        self._name = name
        self._controller = controller
        self._config = config

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

        self._timer = Timer(self._timer_callback, 500)

    def _on_button_click(self) -> None:
        """Show the settings and hide the button after it was clicked."""
        self._settings_window.show()
        self._button.hide()

    @cached_property
    def _settings_window(self) -> QWidget:
        settings_window = MaSettings(self._controller, self._config)
        settings_window.setWindowTitle(f"Configure: {self._name}")
        return settings_window

    def _timer_callback(self) -> None:
        """Show a button in top left corner of painting area."""
        mdiArea = Krita.get_active_mdi_area()
        self._button.move(mdiArea.mapToGlobal(mdiArea.pos()))
        self._button.show()
        self._timer.stop()

    def on_key_press(self) -> None:
        """Start a timer which soon will run a callback once."""
        self._timer.start()

    def on_every_key_release(self) -> None:
        """Hide the button when visible, or cancel the timer if not."""
        self._button.hide()
        self._timer.stop()
