# SPDX-FileCopyrightText: © 2022-2026 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt.QtWidgets import QWidget
from PyQt.QtCore import QPoint


class BaseWidget(QWidget):
    """Adds base convenience methods to the widget."""

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent)

    @property
    def center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self.size().width()//2, self.size().height()//2)

    @property
    def center_global(self) -> QPoint:
        """Return point with center widget's point in screen coordinates."""
        return self.pos() + self.center

    def move_center(self, new_center: QPoint) -> None:
        """Move the widget by providing a new center point."""
        self.move(new_center-self.center)
