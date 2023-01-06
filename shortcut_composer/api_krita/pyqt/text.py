from dataclasses import dataclass
from PyQt5.QtGui import QColor


@dataclass
class Text:

    value: str
    color: QColor = QColor("white")
