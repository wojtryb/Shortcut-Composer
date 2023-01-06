from dataclasses import dataclass
from PyQt5.QtGui import QColor


@dataclass
class Text:
    """Text along with its color."""

    value: str
    color: QColor = QColor("white")
