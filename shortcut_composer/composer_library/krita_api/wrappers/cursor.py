from dataclasses import dataclass

from PyQt5.QtWidgets import QMainWindow


@dataclass
class Cursor:

    qwin: QMainWindow

    @property
    def x(self) -> int:
        return self.qwin.cursor().pos().x()

    @property
    def y(self) -> int:
        return self.qwin.cursor().pos().y()
