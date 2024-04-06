# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol, TypeVar, Generic

from PyQt5.QtCore import Qt, QMimeData, QEvent
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDrag, QPixmap, QMouseEvent, QPaintEvent

from api_krita import Krita
from api_krita.pyqt import Painter, PixmapTransform, BaseWidget
from .label_widget_style import LabelWidgetStyle
from .label_interface import LabelInterface

T = TypeVar("T", bound=LabelInterface, contravariant=True)


class WidgetInstructions(Protocol, Generic[T]):
    """Additional logic to do on entering and leaving a widget."""

    def on_enter(self, label: T) -> None:
        """Logic to perform when mouse starts hovering over widget."""

    def on_leave(self, label: T) -> None:
        """Logic to perform when mouse stops hovering over widget."""


class LabelWidget(BaseWidget, Generic[T]):
    """Displays a LabelInterface data using given style."""

    def __init__(
        self,
        label: T,
        label_widget_style: LabelWidgetStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)

        self.label = label
        self._label_widget_style = label_widget_style

        self.resize(self.icon_radius*2, self.icon_radius*2)
        self.setCursor(Qt.ArrowCursor)

        self._draggable = True
        self._enabled = True
        self._hovered = False
        self._forced = False

        self._instructions: list[WidgetInstructions] = []

    def add_instruction(self, instruction: WidgetInstructions):
        """Add additional logic to do on entering and leaving widget."""
        self._instructions.append(instruction)

    def paintEvent(self, event: QPaintEvent) -> None:
        with Painter(self, event) as painter:
            self.paint(painter)

    def paint(self, painter: Painter):
        """
        Paint the entire widget using the Painter wrapper.

        Paint a background behind a label its border, and image itself.
        """
        # label background
        painter.paint_wheel(
            center=self.center,
            outer_radius=(
                self.icon_radius
                - self._active_indicator_thickness
                - self._label_widget_style.border_thickness//2),
            color=Krita.get_main_color_from_theme())

        # label thin border
        painter.paint_wheel(
            center=self.center,
            outer_radius=self.icon_radius-self._active_indicator_thickness,
            color=self._label_widget_style.border_color,
            thickness=self._label_widget_style.border_thickness)

        # label thick border when label when disabled
        if not self.enabled:
            painter.paint_wheel(
                center=self.center,
                outer_radius=self.icon_radius,
                color=self._label_widget_style.active_color_dark,
                thickness=self._active_indicator_thickness)

        # label thick border when hovered (or it is forced)
        if self.forced or (self._hovered and self.draggable):
            painter.paint_wheel(
                center=self.center,
                outer_radius=self.icon_radius,
                color=self._label_widget_style.active_color,
                thickness=self._active_indicator_thickness)

    @property
    def _active_indicator_thickness(self) -> int:
        return self._label_widget_style.border_thickness*2

    @property
    def draggable(self) -> bool:
        """Return whether the label can be dragged."""
        return self._draggable

    @draggable.setter
    def draggable(self, value: bool) -> None:
        """Make the widget accept dragging or not."""
        if self._draggable == value:
            return
        self._draggable = value
        if value:
            return self.setCursor(Qt.ArrowCursor)
        self.setCursor(Qt.CrossCursor)

    @property
    def enabled(self) -> bool:
        """Return whether the label interacts with mouse hover and drag."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Make the widget interact with mouse or not."""
        if self._enabled == value:
            return
        self._enabled = value
        if not value:
            self.draggable = False
        self.repaint()

    @property
    def forced(self) -> bool:
        """Return whether the widget has forced active color."""
        return self._forced

    @forced.setter
    def forced(self, value: bool) -> None:
        """Make the widget look as it is active even if it is not."""
        if self._forced == value:
            return
        self._forced = value
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
        super().enterEvent(e)
        """Notice that mouse moved over the widget."""
        self._hovered = True
        for instruction in self._instructions:
            instruction.on_enter(self.label)
        self.repaint()

    def leaveEvent(self, e: QEvent) -> None:
        """Notice that mouse moved out of the widget."""
        super().leaveEvent(e)
        self._hovered = False
        for instruction in self._instructions:
            instruction.on_leave(self.label)
        self.repaint()

    @property
    def icon_radius(self) -> int:
        """Return icon radius based flag passed on initialization."""
        return self._label_widget_style.icon_radius
