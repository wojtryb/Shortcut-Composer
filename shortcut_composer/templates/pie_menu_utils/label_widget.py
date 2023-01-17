# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDrag, QPixmap, QMouseEvent

from api_krita.pyqt import PixmapTransform, BaseWidget
from .pie_style import PieStyle
from .label import Label


class LabelWidget(BaseWidget):
    """Displays a `label` inside of `widget` using given `style`."""

    def __init__(
        self,
        label: Label,
        style: PieStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)
        self.setGeometry(0, 0, style.icon_radius*2, style.icon_radius*2)

        self.label = label
        self._style = style
        self.setCursor(Qt.ArrowCursor)

    def move_to_label(self) -> None:
        """Move the widget by providing a new center point."""
        self.move_center(self.label.center)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.buttons() != Qt.LeftButton:
            return

        self.label.activation_progress.set(1)

        drag = QDrag(self)
        drag.setMimeData(QMimeData())

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(PixmapTransform.make_pixmap_round(pixmap))

        drag.exec_(Qt.MoveAction)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.label.activation_progress.set(0)
        return super().mouseReleaseEvent(e)
