# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


from PyQt5.QtWidgets import QWidget

from core_components import Controller
from composer_utils.label import LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget
from composer_utils.label import LabelWidgetStyle
from .pie_label import PieLabel


class PieCurrentValueHolder(QWidget):
    """
    Holds the LabelWidget with the current value.

    - Allows to quickly drag current value to PieMenu.
    - If controller cannot fatch a value, this object is not displayed.
    """

    def __init__(
        self,
        controller: Controller,
        style: LabelWidgetStyle,
    ) -> None:
        super().__init__(None)
        self._controller = controller
        self._style = style
        self._widget: LabelWidget | None = None
        self._is_hidden = True

        self.refresh()
        self.hide()

    # def replace(self, label: PieLabel | None):
    def refresh(self):
        """Replace remembered LabelWidget with the current value."""
        # Leave the widget empty if controller does not get values.
        self._controller.refresh()
        try:
            current_value = self._controller.get_value()
        except NotImplementedError:
            if self._widget is not None:
                self._widget.setParent(None)  # type: ignore
            return

        # Leave the widget empty if the value does not have a label.
        label = PieLabel.from_value(current_value, self._controller)
        if label is None:
            if self._widget is not None:
                self._widget.setParent(None)  # type: ignore
            return

        self._refresh_widget(label)

    def _refresh_widget(self, label: PieLabel) -> None:
        if self._widget is not None:
            self._widget.setParent(None)  # type: ignore

        self._widget = dispatch_label_widget(label)(
            label=label,
            label_widget_style=self._style,
            parent=self)
