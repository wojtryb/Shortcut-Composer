# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QWidget

from ..pie_style import PieStyle
from ..label import Label


class LabelWidget(QWidget):
    """Displays a `label` inside of `widget` using given `style`."""

    def __init__(
        self,
        label: Label,
        style: PieStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)
        self._label = label
        self._parent = parent
        self._style = style
        self.setCursor(Qt.DragMoveCursor)

        size = self._style.icon_radius*2
        self.setGeometry(0, 0, size, size)

    @property
    def center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._style.icon_radius, self._style.icon_radius)

    def move_to_label(self) -> None:
        """Move the widget by providing a new center point."""
        self.move(self._label.center-self.center)  # type: ignore
