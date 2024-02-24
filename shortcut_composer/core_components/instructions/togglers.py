# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from api_krita.enums import Toggle
from ..instruction_base import Instruction


def _set_up(self) -> None:
    """Set a krita action's state to `True`."""
    self.toggle.state = True


def _set_down(self) -> None:
    """Set a krita action's state to `False`."""
    self.toggle.state = False


@dataclass
class _ToggleInstruction(Instruction):
    """Instruction which handles a given krita action."""
    toggle: Toggle


class EnsureOn(_ToggleInstruction):
    """
    Set given krita action to `True` on each key press.

    ### Example usage:
    ```python
    # Make canvas mirrored when key is pressed.
    instructions.EnsureOn(Toggle.MIRROR_CANVAS)
    ```
    """
    on_key_press = _set_up


class EnsureOff(_ToggleInstruction):
    """
    Set given krita action to `False` on each key press.

    ### Example usage:
    ```python
    # Make canvas not mirrored when key is pressed.
    instructions.EnsureOff(Toggle.MIRROR_CANVAS)
    ```
    """
    on_key_press = _set_down


class TemporaryOn(_ToggleInstruction):
    """
    Set given krita action to `True` between key press and release.

    ### Example usage:
    ```python
    # Make canvas mirrored on key press and not mirrored on release.
    instructions.TemporaryOn(Toggle.MIRROR_CANVAS)
    ```
    """
    on_key_press = _set_up
    on_every_key_release = _set_down


class TemporaryOff(_ToggleInstruction):
    """
    Set given krita action to `False` between key press and release.

    ### Example usage:
    ```python
    # Make canvas not mirrored on key press and mirrored on release.
    instructions.TemporaryOn(Toggle.MIRROR_CANVAS)
    ```
    """
    on_key_press = _set_down
    on_every_key_release = _set_up
