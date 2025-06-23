# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


from PyQt5.QtWidgets import QWidget

from composer_utils.label import LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget
from composer_utils.label import LabelWidgetStyle
from .pie_label import PieLabel


# LabelHolder
class PieCurrentValueHolder(QWidget):
    """
    Holds the LabelWidget with the current value.

    - Allows to quickly drag current value to PieMenu.
    - If controller cannot fatch a value, this object is not displayed.
    """

    def __init__(
        self,
        style: LabelWidgetStyle,
    ) -> None:
        super().__init__(None)
        self._style = style
        self._widget: LabelWidget | None = None
        self._enabled = False

    def replace(self, label: PieLabel | None) -> None:
        """Replace remembered LabelWidget with the passed value."""
        if self._widget is not None:
            self._widget.setParent(None)  # type: ignore

        if label is None:
            return

        self._widget = dispatch_label_widget(label)(
            label=label,
            label_widget_style=self._style,
            parent=self)
        self._widget.enabled = self._enabled
        self._widget.draggable = self._enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if self._widget is not None:
            self._widget.enabled = self._enabled
            self._widget.draggable = self._enabled
