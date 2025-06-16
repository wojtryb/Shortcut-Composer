# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


from PyQt5.QtCore import QPoint

from core_components import Controller
from composer_utils.label import LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget
from .pie_label import PieLabel
from .pie_widget import PieWidget
from .pie_style_holder import PieStyleHolder


class PieCurrentValueHolder:
    """
    Holds the LabelWidget with the current value.

    - Allows to quickly drag current value to PieMenu.
    - If controller cannot fatch a value, this object is not displayed.
    - Can be hidden and shown similarily to QWidget.
    """

    def __init__(
        self,
        controller: Controller,
        style: PieStyleHolder,
        pie_widget: PieWidget
    ) -> None:
        self._controller = controller
        self._style = style
        self._pie_widget = pie_widget
        self._widget: LabelWidget | None = None
        self._is_hidden = True

        self.refresh()
        self.hide()

    def refresh(self):
        """Replace remembered LabelWidget with the current value."""
        # Leave the widget empty if controller does not get values.
        try:
            current_value = self._controller.get_value()
        except NotImplementedError:
            return

        # Leave the widget empty if the value does not have a label.
        label = PieLabel.from_value(current_value, self._controller)
        if label is None:
            return

        if self._widget is not None:
            self._widget.setParent(None)  # type: ignore
        self._widget = dispatch_label_widget(label)(
            label=label,
            label_widget_style=self._style.button_size_label_style,
            parent=self._pie_widget)
        self._ensure_correct_position()
        if self._is_hidden:
            self.hide()

    def hide(self):
        """Do not display the widget until the `show()` is called."""
        self._is_hidden = True
        if self._widget is not None:
            self._widget.hide()

    def show(self):
        """Display the widget until the `hide` is called."""
        self._is_hidden = False
        if self._widget is not None:
            self._widget.show()

    def _ensure_correct_position(self):
        """Move the widget to the bottom-right spot of the PieWidget."""
        if self._widget is not None:
            self._widget.move(QPoint(
                self._pie_widget.width()-self._widget.width(),
                self._pie_widget.height()-self._widget.height()))
