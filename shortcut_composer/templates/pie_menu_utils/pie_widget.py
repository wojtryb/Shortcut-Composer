# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPaintEvent

from api_krita.pyqt import Painter
from .pie_style import PieStyle
from .label_holder import LabelHolder
from .drag_widget import DragWidget
from .pie_painter import PiePainter


class PieWidget(DragWidget):
    """
    PyQt5 widget with icons on ring that can be selected by hovering.

    Methods inherits from QWidget used by other components:
    - show() - displays the widget
    - hide() - hides the widget
    - repaint() - updates widget display after its data was changed

    Overrides paintEvent(QPaintEvent) which tells how the widget looks

    - Paints the widget: its base, and active pie and deadzone indicator
    - Wraps Labels with LabelWidgets which activated, paint them
    - Extends widget interface to allow moving the widget on screen by
      providing the widget center.
    """

    def __init__(
        self,
        labels: LabelHolder,
        style: PieStyle,
        parent=None
    ):
        super().__init__(labels, style, parent)
        self.labels = labels
        self._style = style

        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Popup |
            Qt.FramelessWindowHint |
            Qt.NoDropShadowWindowHint))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CrossCursor)

        size = self._style.widget_radius*2
        self.setGeometry(0, 0, size, size)

    @property
    def _center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self.size().width()//2, self.size().height()//2)

    @property
    def center_global(self) -> QPoint:
        """Return point with center widget's point in screen coordinates."""
        return self.pos() + self._center  # type: ignore

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._style.deadzone_radius

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            PiePainter(painter, self.labels, self._style)

    def move_center(self, new_center: QPoint) -> None:
        """Move the widget by providing a new center point."""
        self.move(new_center-self._center)  # type: ignore
