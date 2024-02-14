# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
# FIXME: move to common
from shortcut_composer.core_components.controller_base import Controller
from .rotation_widget import RotationWidget

Zone = RotationWidget.Zone


class RotationActuator:
    def __init__(
        self,
        rotation_widget: RotationWidget,
        controller: Controller[int],
        modifier: Callable[[int], int] = lambda x: x,
    ) -> None:
        self._rotation_widget = rotation_widget
        self._controller = controller
        self._modifier = modifier

        self._timer = Timer(self._update, Config.get_sleep_time())

    def start(self):
        self._center_global = QCursor().pos()
        self._starting_value = self._controller.get_value()

        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def _update(self) -> None:
        if self._rotation_widget.selected_zone == Zone.DEADZONE:
            value = self._starting_value
        else:
            value = self._rotation_widget.selected_angle
        modified = self._modifier(value)
        self._controller.set_value(modified)
