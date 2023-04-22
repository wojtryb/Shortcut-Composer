from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtWidgets import QWidget, QPushButton

trigger = pyqtSignal()


class SafeConfirmButton(QPushButton):

    clicked = pyqtSignal()  # type: ignore

    def __init__(
        self,
        icon: QIcon = QIcon(),
        text: str = "",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(icon, text, parent)
        super().clicked.connect(self._clicked)
        self._main_text = text
        self.hover_text: Optional[str] = None
        self._confirm_mode = False

    def _clicked(self) -> None:
        if self._confirm_mode:
            self._confirm_mode = False
            return self.clicked.emit()
        self._confirm_mode = True

    @property
    def _confirm_mode(self):
        return self.__confirm_mode

    @_confirm_mode.setter
    def _confirm_mode(self, value: bool):
        if value is True:
            self.setText("Confirm")
            self.setStyleSheet(
                "border-style: solid;"
                "border-color: Tomato;"
                "border-width: 1px")
        else:
            super().setText(self._main_text)
            self.setStyleSheet("")
        self.__confirm_mode = value

    @property
    def main_text(self):
        return self._main_text

    @main_text.setter
    def main_text(self, text):
        self._main_text = text
        self.setText(self._main_text)

    def enterEvent(self, a0: QEvent) -> None:
        if self.hover_text is not None:
            self.setText(self.hover_text)
        return super().enterEvent(a0)

    def leaveEvent(self, e: QEvent) -> None:
        self._confirm_mode = False
        return super().leaveEvent(e)
