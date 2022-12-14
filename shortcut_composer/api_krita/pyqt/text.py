from dataclasses import dataclass
from PyQt5.QtGui import QColor


@dataclass
class Text:

    text: str
    color: QColor = QColor("white")
