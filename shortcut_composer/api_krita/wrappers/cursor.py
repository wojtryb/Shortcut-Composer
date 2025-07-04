# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

try:
    from PyQt5.QtWidgets import QMainWindow
except ModuleNotFoundError:
    from PyQt6.QtWidgets import QMainWindow


@dataclass
class Cursor:
    """Wraps Qt cursor for typing, documentation and PEP8 compatibility."""

    q_win: QMainWindow

    def x(self) -> int:
        """Return x axis of cursor in pixels in relation to screen."""
        try:
            return self.q_win.cursor().pos().x()
        except AttributeError:
            return self.q_win.cursor().position().x()

    def y(self) -> int:
        """Return y axis of cursor in pixels in relation to screen."""
        try:
            return self.q_win.cursor().pos().y()
        except AttributeError:
            return self.q_win.cursor().position().y()
