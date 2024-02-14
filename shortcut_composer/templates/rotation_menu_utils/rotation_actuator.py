# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
from shortcut_composer.core_components.controller_base import Controller
from .rotation_widget import RotationWidget
from .rotation_widget_state import Zone
from .rotation_config import RotationConfig


class RotationActuator:
    def __init__(
        self,
        rotation_widget: RotationWidget,
        controller: Controller[int],
        config: RotationConfig,
    ) -> None:
        self._rotation_widget = rotation_widget
        self._controller = controller
        self._config = config

        self._timer = Timer(self._update, Config.get_sleep_time())

    def start(self):
        self._center_global = QCursor().pos()
        self._starting_value = self._reverse_modifier(
            self._controller.get_value())

        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def _update(self) -> None:
        if self._rotation_widget.state.selected_zone == Zone.DEADZONE:
            value = self._starting_value
        else:
            value = self._rotation_widget.state.selected_angle
        modified = self._modifier(value)
        self._controller.set_value(modified)

    def _modifier(self, value: int):
        sign = -1 if self._config.IS_COUNTERCLOCKWISE.read() else 1
        return sign*(value - self._config.OFFSET.read())

    def _reverse_modifier(self, value: int):
        sign = -1 if self._config.IS_COUNTERCLOCKWISE.read() else 1
        return sign*value + self._config.OFFSET.read()
