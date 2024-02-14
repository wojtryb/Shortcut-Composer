# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional
from core_components import Controller, Instruction
from .raw_instructions import RawInstructions
from .rotation_menu_utils import RotationManager, RotationConfig


class RotationMenu(RawInstructions):
    def __init__(
        self, *,
        name: str,
        controller: Controller[int],
        instructions: Optional[List[Instruction]] = None,
        counterclockwise: bool = False,
        offset: int = 0,
        deadzone_scale: float = 1.0,
        free_zone_scale: float = 1.0,
        divisions: int = 24,
        short_vs_long_press_time: Optional[float] = None,
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)
        self._controller = controller

        self._config = RotationConfig(
            name=self.name,
            deadzone_scale=deadzone_scale,
            free_zone_scale=free_zone_scale,
            divisions=divisions)

        sign = -1 if counterclockwise else 1
        self._rotation_manager = RotationManager(
            config=self._config,
            controller=controller,
            modifier=lambda x: sign*x + offset)

    def on_key_press(self) -> None:
        """Handle the event of user pressing the action key."""
        super().on_key_press()
        self._controller.refresh()
        self._rotation_manager.start()

    def on_every_key_release(self) -> None:
        """Handle the key release event."""
        super().on_every_key_release()
        self._rotation_manager.stop()
