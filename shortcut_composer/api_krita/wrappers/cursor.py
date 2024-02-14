# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from PyQt5.QtWidgets import QMainWindow


@dataclass
class Cursor:
    """Wraps Qt5 cursor for typing, documentation and PEP8 compatibility."""

    q_win: QMainWindow

    def x(self) -> int:
        """Return x axis of cursor in pixels in relation to screen."""
        return self.q_win.cursor().pos().x()

    def y(self) -> int:
        """Return y axis of cursor in pixels in relation to screen."""
        return self.q_win.cursor().pos().y()
