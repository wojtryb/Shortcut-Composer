# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time

from PyQt5.QtGui import QKeyEvent

from ..complex_action_interface import ComplexActionInterface


class ShortcutAdapter:
    """
    Adds additional key events based on krita's key press and release.

    Krita events:
    - on_key_press (connected to trigger of krita action)
    - on_key_release (intercepted with event filter)

    Custom action events:
    - on_key_press
    - on_short_key_release (release directly after the press)
    - on_long_key_release (release long time after the press)
    - on_every_key_release (called after short or long release callback)

    Only one instance of ShortcutAdapter can handle key at a time. All
    others are blocked.
    """

    def __init__(self, action: ComplexActionInterface) -> None:
        self.action = action
        self.local_lock = False
        self.last_press_time = time()

    def on_key_press(self) -> None:
        """Run action's on_key_press() and remember the time of it."""
        self.local_lock = True
        self.last_press_time = time()
        self.action.on_key_press()

    def event_filter_callback(self, release_event: QKeyEvent) -> None:
        """Handle key release if the event is related to the action."""
        if self.local_lock and not release_event.isAutoRepeat():
            self._on_key_release()

    def _on_key_release(self) -> None:
        """Run proper key release methods based on time elapsed from press."""
        elapsed_time = time() - self.last_press_time
        if elapsed_time < self.action.short_vs_long_press_time:
            self.action.on_short_key_release()
        else:
            self.action.on_long_key_release()
        self.action.on_every_key_release()
        self.local_lock = False
