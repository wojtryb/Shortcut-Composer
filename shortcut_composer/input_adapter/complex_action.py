# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from composer_utils import Config
from core_components import InstructionHolder, Instruction


class ComplexAction:
    """
    Stores basic action attributes and grants main plugin action interface.

    ### Arguments:

    - `name`         -- unique name of action. Must match the definition
                        in shortcut_composer.action file
    - `instructions` -- (optional) list of additional instructions to
                        perform on key press and release.
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long.

    Class is meant for creating child classes which override:
    - on_key_press
    - on_short_key_release
    - on_long_key_release
    - on_every_key_release
    """

    def __init__(
        self, *,
        name: str,
        instructions: List[Instruction] = [],
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        self.name = name
        self.short_vs_long_press_time = _read_time(short_vs_long_press_time)
        self._instructions = InstructionHolder(instructions)

    def on_key_press(self) -> None:
        """Called on each press of key specified in settings."""
        self._instructions.on_key_press()

    def on_short_key_release(self) -> None:
        """Called when related key was released shortly after press."""
        self._instructions.on_short_key_release()

    def on_long_key_release(self) -> None:
        """Called when related key was released after a long time."""
        self._instructions.on_long_key_release()

    def on_every_key_release(self) -> None:
        """Called on each release of related key, after short/long callback."""
        self._instructions.on_every_key_release()


def _read_time(short_vs_long_press_time: Optional[float]) -> float:
    """Return the given time, or time red from krita config if not given."""
    if short_vs_long_press_time is None:
        return Config.SHORT_VS_LONG_PRESS_TIME.read()
    return short_vs_long_press_time
