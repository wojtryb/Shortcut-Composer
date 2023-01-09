# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPaintEvent

from api_krita.pyqt import AnimatedWidget, Painter
from composer_utils import Config
from .pie_style import PieStyle
from .label import LabelPainter
from .label_holder import LabelHolder


class PieWidget(AnimatedWidget):
    """
    PyQt5 widget with icons on ring that can be selected by hovering.

    Methods inherits from QWidget used by other components:
    - show() - displays the widget
    - hide() - hides the widget
    - repaint() - updates widget display after its data was changed

    Overrides paintEvent(QPaintEvent) which tells how the widget looks

    - Paints the widget: its base, and active pie and deadzone indicator
    - Wraps Labels with LabelPainter which activated, paint them
    - Extends widget interface to allow moving the widget on screen by
      providing the widget center.
    """

    def __init__(
        self,
        labels: LabelHolder,
        style: PieStyle,
        parent=None
    ):
        super().__init__(parent, Config.PIE_ANIMATION_TIME.read())
        self.labels = labels
        self._style = style
        self._label_painters = self._create_label_painters()

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
    def center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self._style.widget_radius, self._style.widget_radius)

    @property
    def center_global(self) -> QPoint:
        """Return point with center widget's point in screen coordinates."""
        return self.pos() + self.center  # type: ignore

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._style.deadzone_radius

    def move_center(self, new_center: QPoint) -> None:
        """Move the widget by providing a new center point."""
        self.move(new_center-self.center)  # type: ignore

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            self._paint_deadzone_indicator(painter)
            self._paint_base_wheel(painter)
            self._paint_active_pie(painter)
            self._paint_base_border(painter)

            for label_painter in self._label_painters:
                label_painter.paint(painter)

    def _paint_base_wheel(self, painter: Painter) -> None:
        """Paint a base circle and low opacity background to trick Windows."""
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._style.no_border_radius,
            color=QColor(128, 128, 128, 1),
        )
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._style.no_border_radius,
            color=self._style.background_color,
            thickness=self._style.area_thickness,
        )

    def _paint_base_border(self, painter: Painter) -> None:
        """Paint a border on the inner edge of base circle."""
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._style.inner_edge_radius,
            color=self._style.border_color,
            thickness=self._style.border_thickness,
        )

    def _paint_deadzone_indicator(self, painter: Painter) -> None:
        """Paint the circle representing deadzone, when its valid."""
        if self.deadzone == float("inf"):
            return

        painter.paint_wheel(
            center=self.center,
            outer_radius=self.deadzone,
            color=QColor(128, 255, 128, 120),
            thickness=1,
        )
        painter.paint_wheel(
            center=self.center,
            outer_radius=self.deadzone-1,
            color=QColor(255, 128, 128, 120),
            thickness=1,
        )

    def _paint_active_pie(self, painter: Painter) -> None:
        """Paint a pie representing active label if there is one."""
        if not self.labels.active:
            return

        painter.paint_pie(
            center=self.center,
            outer_radius=self._style.no_border_radius,
            angle=self.labels.active.angle,
            span=360//len(self._label_painters),
            color=self._style.active_color,
            thickness=self._style.area_thickness,
        )

    def _create_label_painters(self) -> List[LabelPainter]:
        """Wrap all labels with LabelPainter which can paint it."""
        return [label.get_painter(self, self._style) for label in self.labels]
