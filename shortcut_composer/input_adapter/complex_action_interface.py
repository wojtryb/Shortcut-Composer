# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Protocol


class ComplexActionInterface(Protocol):
    """
    Interface of the main plugin action.

    - `name` -- unique name of action. Must match the definition in
                shortcut_composer.action file
    - `short_vs_long_press_time` -- time [s] that specifies if key press
                                    is short or long.
    """

    name: str
    short_vs_long_press_time: float

    def on_key_press(self) -> None:
        """Called on each press of key specified in settings."""

    def on_short_key_release(self) -> None:
        """Called when related key was released shortly after press."""

    def on_long_key_release(self) -> None:
        """Called when related key was released after a long time."""

    def on_every_key_release(self) -> None:
        """Called on each release of related key, after short/long callback."""