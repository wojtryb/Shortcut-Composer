# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QCursor
from api_krita.pyqt import Timer

from composer_utils import Config
from config_system import Field
from data_components import RotationDeadzoneStrategy
from shortcut_composer.core_components.controller_base import Controller
from .rotation_widget import RotationWidget
from .rotation_widget_state import Zone
from .rotation_config import RotationConfig


class RotationActuator:
    """
    Contiguously activates the selected angle in the widget.

    Actuator tracks selected strategy using `strategy_field` passed on
    initialization. It can be changed in runtime.
    """

    def __init__(
        self,
        rotation_widget: RotationWidget,
        controller: Controller[int],
        config: RotationConfig,
        strategy_field: Field,
    ) -> None:
        self._rotation_widget = rotation_widget
        self._controller = controller
        self._config = config

        def update_strategy():
            self._strategy = strategy_field.read()
        self._strategy: RotationDeadzoneStrategy
        strategy_field.register_callback(update_strategy)
        update_strategy()

        self._timer = Timer(self._update, Config.get_sleep_time())

    def start(self):
        """Start loop of contiguous value setting."""
        self._center_global = QCursor().pos()
        self._starting_value = self._reverse_modifier(
            self._controller.get_value())

        self._timer.start()

    def stop(self) -> None:
        """Start the loop of contiguous value setting."""
        self._timer.stop()

    def _update(self) -> None:
        """Set the angle considering deadzone strategy and value modifier."""
        if self._rotation_widget.state.selected_zone == Zone.DEADZONE:
            if self._strategy == RotationDeadzoneStrategy.KEEP_CHANGE:
                return
            elif self._strategy == RotationDeadzoneStrategy.DISCARD_CHANGE:
                value = self._starting_value
            else:  # RotationDeadzoneStrategy.SET_ZERO
                self._controller.set_value(0)
                return
        else:
            value = self._rotation_widget.state.selected_angle
        modified = self._modifier(value)
        self._controller.set_value(modified)

    def _modifier(self, value: int):
        """Transforms angle to value considering sign and offset."""
        sign = -1 if self._config.IS_COUNTERCLOCKWISE.read() else 1
        return sign*(value - self._config.OFFSET.read())

    def _reverse_modifier(self, value: int):
        """Transforms value to angle."""
        sign = -1 if self._config.IS_COUNTERCLOCKWISE.read() else 1
        return sign*value + self._config.OFFSET.read()
