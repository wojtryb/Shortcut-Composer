# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtWidgets import QWidget, QPushButton


class SafeConfirmButton(QPushButton):
    """
    Button that requires repeating click to confirm first one was intentional.

    After first click, the border is changed, and button changes its
    label to "Confirm".

    Moving the mouse out of the button aborts the confirmation mode.
    """

    clicked = pyqtSignal()  # type: ignore
    _empty_icon = QIcon()

    def __init__(
        self,
        icon: QIcon = QIcon(),
        text: str = "",
        confirm_text: str = "Confirm?",
        parent: QWidget | None = None
    ) -> None:
        super().__init__(icon, text, parent)
        super().clicked.connect(self._clicked)
        self._main_text = text
        self.confirm_text = confirm_text
        self._icon = icon
        self._confirm_mode = False

    def _clicked(self) -> None:
        """Enter the confirmation mode. If already there, forward the click."""
        if self._confirm_mode:
            self._confirm_mode = False
            return self.clicked.emit()
        self._confirm_mode = True

    @property
    def _confirm_mode(self) -> bool:
        """Return whether in confirmation mode."""
        return self.__confirm_mode

    @_confirm_mode.setter
    def _confirm_mode(self, value: bool) -> None:
        """Set mode. Confirmation mode requires red border and other text."""
        if value is True:
            self.setText(self.confirm_text)
            self.setIcon(self._empty_icon)
            self.setStyleSheet(
                "border-style: solid;"
                "border-color: Tomato;"
                "border-radius: 3px;"
                "border-width: 1px")
        else:
            self.setText(self._main_text)
            self.setIcon(self._icon)
            self.setStyleSheet("")
        self.__confirm_mode = value

    @property
    def main_text(self) -> str:
        """Return the text displayed when not in confirmation mode."""
        return self._main_text

    @main_text.setter
    def main_text(self, text: str) -> None:
        """Set the text displayed when not in confirmation mode."""
        self._main_text = text
        self.setText(self._main_text)

    @property
    def icon(self) -> QIcon:
        """Return the icon displayed when not in confirmation mode."""
        return self._icon

    @icon.setter
    def icon(self, icon: QIcon) -> None:
        """Set the icon displayed when not in confirmation mode."""
        self._icon = icon
        self.setIcon(self._icon)

    def leaveEvent(self, e: QEvent) -> None:
        """Abort confirmation mode when mouse leaves the button."""
        self._confirm_mode = False
        super().leaveEvent(e)
