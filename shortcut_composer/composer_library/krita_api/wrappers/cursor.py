from dataclasses import dataclass

from PyQt5.QtWidgets import QMainWindow


@dataclass
class Cursor:

    qwin: QMainWindow

    def x(self) -> int:
        return self.qwin.cursor().pos().x()

    def y(self) -> int:
        return self.qwin.cursor().pos().y()
