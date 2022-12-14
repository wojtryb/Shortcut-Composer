from typing import Union, Any
from dataclasses import dataclass

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPoint

from api_krita.pyqt import Text


@dataclass
class Label:

    value: Any
    center: QPoint = QPoint(0, 0)
    angle: int = 0
    display_value: Union[QPixmap, Text, None] = None

    @property
    def text(self) -> Optional[Text]:
        if isinstance(self.display_value, Text):
            return self.display_value

    @property
    def image(self) -> Optional[QPixmap]:
        if isinstance(self.display_value, QPixmap):
            return self.display_value
