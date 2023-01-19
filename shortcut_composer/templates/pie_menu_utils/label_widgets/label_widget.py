# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import QPoint, Qt, QMimeData
from PyQt5.QtWidgets import QWidget

from ..pie_style import PieStyle
from ..label import Label

from PyQt5.QtGui import QDrag, QPixmap
from api_krita.pyqt import PixmapTransform


class LabelWidget(QWidget):
    """Displays a `label` inside of `widget` using given `style`."""

    def __init__(
        self,
        label: Label,
        style: PieStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)
        self.label = label
        self._parent = parent
        self._style = style
        self.setCursor(Qt.ArrowCursor)

        size = self._style.icon_radius*2
        self.setGeometry(0, 0, size, size)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        drag = QDrag(self)
        drag.setMimeData(QMimeData())

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(PixmapTransform.make_pixmap_round(pixmap))

        drag.exec_(Qt.MoveAction)

    @property
    def center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._style.icon_radius, self._style.icon_radius)

    def move_to_label(self) -> None:
        """Move the widget by providing a new center point."""
        self.move(self.label.center-self.center)  # type: ignore
