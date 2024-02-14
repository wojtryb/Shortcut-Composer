# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import Config
# FIXME: move to common
from shortcut_composer.core_components.controller_base import Controller
from .rotation_widget import RotationWidget
from .rotation_config import RotationConfig

Zone = RotationWidget.Zone


def snap_degree(value: int, step_size: int) -> int:
    if not 0 < step_size <= 360:
        raise RuntimeError("Step needs to be in range (0, 360>")

    moved_by_half_of_step = value + step_size//2
    snapped = moved_by_half_of_step // step_size * step_size

    return snapped % 360


class RotationActuator:
    def __init__(
        self,
        rotation_widget: RotationWidget,
        config: RotationConfig,
        controller: Controller[int],
        modifier: Callable[[int], int] = lambda x: x,
    ) -> None:
        self._rotation_widget = rotation_widget
        self._config = config
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

        def snap_angle():
            return self._modifier(snap_degree(
                value=self._rotation_widget.selected_angle,
                step_size=360//self._config.DIVISIONS.read()))

        def free_angle():
            return self._modifier(self._rotation_widget.selected_angle)

        inner_zone = snap_angle
        outer_zone = free_angle
        if self._config.INVERSE_ZONES.read():
            inner_zone, outer_zone = outer_zone, inner_zone

        if self._rotation_widget.selected_zone == Zone.DEADZONE:
            to_set = self._starting_value
        elif self._rotation_widget.selected_zone == Zone.INNER_ZONE:
            to_set = inner_zone()
        else:
            to_set = outer_zone()

        self._controller.set_value(to_set)
