from dataclasses import dataclass

from PyQt5.QtWidgets import QMainWindow


@dataclass
class Cursor:

    qwin: QMainWindow

    @property
    def x(self):
        return self.qwin.cursor().pos().x()

    @property
    def y(self):
        return self.qwin.cursor().pos().y()
