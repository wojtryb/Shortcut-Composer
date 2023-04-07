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
        is_unscaled: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setGeometry(0, 0, style.icon_radius*2, style.icon_radius*2)
        self.label = label
        self._style = style
        self._is_unscaled = is_unscaled

        self._draggable = True
        self.draggable = self._draggable

        self._enabled = True
        self._hovered = False

    @property
    def draggable(self):
        return self._draggable

    @draggable.setter
    def draggable(self, value: bool):
        self._draggable = value
        if value:
            return self.setCursor(Qt.ArrowCursor)
        self.setCursor(Qt.CrossCursor)

    def move_to_label(self) -> None:
        """Move the widget by providing a new center point."""
        self.move_center(self.label.center)

    def set_enabled(self, value: bool):
        self._enabled = value
        if not value:
            self._draggable = False
        self.repaint()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """Initiate a drag loop for this Widget, so Widgets can be swapped."""
        if e.buttons() != Qt.LeftButton or not self._draggable:
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
        if not self._enabled:
            return self._style.active_color_dark
        if self._hovered and self.draggable:
            return self._style.active_color
        return self._style.border_color

    @property
    def icon_radius(self):
        if self._is_unscaled:
            return self._style.unscaled_icon_radius
        return self._style.icon_radius
