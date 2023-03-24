# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt, QMimeData, QEvent
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
        self.draggable = True

        self.label = label
        self._style = style
        self._hovered = False
        self.setCursor(Qt.ArrowCursor)

    def move_to_label(self) -> None:
        """Move the widget by providing a new center point."""
        self.move_center(self.label.center)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """Initiate a drag loop for this Widget, so Widgets can be swapped."""
        if e.buttons() != Qt.LeftButton or not self.draggable:
            return

        drag = QDrag(self)
        drag.setMimeData(QMimeData())

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(PixmapTransform.make_pixmap_round(pixmap))

        drag.exec_(Qt.MoveAction)

    def enterEvent(self, e: QEvent) -> None:
        self._hovered = True
        self.repaint()
        return super().enterEvent(e)

    def leaveEvent(self, e: QEvent) -> None:
        self._hovered = False
        self.repaint()
        return super().leaveEvent(e)

    @property
    def _border_color(self):
        if self._hovered and self.draggable:
            return self._style.active_color_dark
        return self._style.border_color
