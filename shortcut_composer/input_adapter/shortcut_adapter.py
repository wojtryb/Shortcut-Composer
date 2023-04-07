# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time

from PyQt5.QtGui import QKeyEvent, QKeySequence

from .api_krita import Krita
from .complex_action_interface import ComplexActionInterface


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
    """

    def __init__(self, action: ComplexActionInterface) -> None:
        self.action = action
        self.key_released = True
        self.last_press_time = time()

    def on_key_press(self) -> None:
        """Run action's on_key_press() and remember the time of it."""
        self.key_released = False
        self.last_press_time = time()
        self.action.on_key_press()

    def _on_key_release(self) -> None:
        """Run proper key release methods based on time elapsed from press."""
        self.key_released = True
        if time() - self.last_press_time < self._short_vs_long_press_time:
            self.action.on_short_key_release()
        else:
            self.action.on_long_key_release()
        self.action.on_every_key_release()

    def _is_event_key_release(self, release_event: QKeyEvent) -> bool:
        """Decide if the key release event is matches shortcut and is valid."""
        return (not release_event.isAutoRepeat()
                and not self.key_released
                and self._match_shortcuts(
                    self._key_sequence_from_event(release_event),
                    self.tool_shortcut))

    def event_filter_callback(self, release_event: QKeyEvent) -> None:
        """Handle key release if the event is related to the action."""
        if self._is_event_key_release(release_event):
            self._on_key_release()

    @property
    def _short_vs_long_press_time(self) -> float:
        """Time in seconds distinguishing short key presses from long ones."""
        return self.action.short_vs_long_press_time

    @property
    def tool_shortcut(self) -> QKeySequence:
        """Return shortcut assigned to shortcut red from krita settings."""
        return Krita.get_action_shortcut(self.action.name)

    @staticmethod
    def _key_sequence_from_event(event: QKeyEvent):
        return QKeySequence(event.modifiers() | event.key())  # type: ignore

    @staticmethod
    def _match_shortcuts(_a: QKeySequence, _b: QKeySequence, /) -> bool:
        """Custom match pattern - one string is preset in another one."""
        parsed_a = _a.toString()
        parsed_b = _b.toString()
        return parsed_a in parsed_b or parsed_b in parsed_a
