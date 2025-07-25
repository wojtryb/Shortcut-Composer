# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QDragEnterEvent, QDragLeaveEvent

from ..label_widget import LabelWidget
from ..label_widget_style import LabelWidgetStyle
from ..label_widget_impl import dispatch_label_widget
from ..label_interface import LabelInterface


class LabelHolder(QWidget):
    """
    Holds the LabelWidget with the current value.

    - Allows to quickly drag current value to PieMenu.
    - If controller cannot fatch a value, this object is not displayed.
    """

    def __init__(
        self,
        style: LabelWidgetStyle = LabelWidgetStyle(),
        allowed_types: type | tuple[type, ...] = object,
    ) -> None:
        super().__init__(None)
        self._style = style
        self._allowed_types = allowed_types

        self._widget: LabelWidget | None = None
        self._enabled = False
        self._previous_label: LabelInterface | None = None

        self.setAcceptDrops(True)
        self.reset_size()

    def replace(self, label: LabelInterface | None) -> None:
        """Replace remembered LabelWidget with the passed value."""
        if self._widget is not None:
            self._widget.setParent(None)  # type: ignore

        if label is None:
            return

        self._update_with_label(label)

    @property
    def label(self) -> LabelInterface | None:
        if self._widget is not None:
            return self._widget.label
        return None

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if self._widget is not None:
            self._widget.enabled = self._enabled
            self._widget.draggable = self._enabled

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Allow dragging the widgets while in edit mode."""
        e.accept()
        source_widget = e.source()

        if not isinstance(source_widget, LabelWidget):
            # Drag incoming from outside the PieWidget ecosystem
            return

        label = source_widget.label
        if not isinstance(label.value, self._allowed_types):
            # Label type does not match the type of pie menu
            return

        if self._widget is not None:
            self._previous_label = self._widget.label

        self._update_with_label(label)

    def dragLeaveEvent(self, e: QDragLeaveEvent) -> None:
        """Remove the label when its widget is dragged out."""
        if self._previous_label is not None:
            self._update_with_label(self._previous_label)
        return super().dragLeaveEvent(e)

    def _update_with_label(self, label: LabelInterface):
        self._widget = dispatch_label_widget(label)(
            label=label,
            label_widget_style=self._style,
            parent=self)
        self._widget.enabled = self._enabled
        self._widget.draggable = self._enabled
        self._widget.show()

    def reset_size(self) -> None:
        """Set widget geometry according to style."""
        diameter = 2*self._style.icon_radius
        self.setFixedSize(diameter, diameter)
