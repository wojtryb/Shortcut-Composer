# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional
from core_components import Controller, Instruction
from .raw_instructions import RawInstructions
from .rotation_menu_utils import (
    RotationActuator,
    RotationManager,
    RotationConfig,
    RotationWidget)


class RotationMenu(RawInstructions):
    def __init__(
        self, *,
        name: str,
        controller: Controller[int],
        instructions: Optional[List[Instruction]] = None,
        counterclockwise: bool = False,
        offset: int = 0,
        deadzone_scale: float = 1.0,
        inner_zone_scale: float = 1.0,
        divisions: int = 24,
        inverse_zones: bool = False,
        short_vs_long_press_time: Optional[float] = None,
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)
        self._controller = controller

        self._config = RotationConfig(
            name=self.name,
            deadzone_scale=deadzone_scale,
            inner_zone_scale=inner_zone_scale,
            divisions=divisions,
            inverse_zones=inverse_zones)

        self._rotation_widget = RotationWidget(config=self._config)

        self._rotation_manager = RotationManager(
            rotation_widget=self._rotation_widget,
            config=self._config)

        sign = -1 if counterclockwise else 1
        self._rotation_actuator = RotationActuator(
            rotation_widget=self._rotation_widget,
            config=self._config,
            controller=controller,
            modifier=lambda x: sign*x + offset)

    def on_key_press(self) -> None:
        """Handle the event of user pressing the action key."""
        super().on_key_press()
        self._controller.refresh()
        self._rotation_manager.start()
        self._rotation_actuator.start()

    def on_every_key_release(self) -> None:
        """Handle the key release event."""
        super().on_every_key_release()
        self._rotation_actuator.stop()
        self._rotation_manager.stop()
