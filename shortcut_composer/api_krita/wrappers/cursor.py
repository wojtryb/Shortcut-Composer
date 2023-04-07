# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from PyQt5.QtWidgets import QMainWindow


@dataclass
class Cursor:
    """Wraps Qt5 cursor for typing, documentation and PEP8 compatibility."""

    qwin: QMainWindow

    def x(self) -> int:
        """Return x axis of cursor in pixels in relation to screen."""
        return self.qwin.cursor().pos().x()

    def y(self) -> int:
        """Return y axis of cursor in pixels in relation to screen."""
        return self.qwin.cursor().pos().y()
