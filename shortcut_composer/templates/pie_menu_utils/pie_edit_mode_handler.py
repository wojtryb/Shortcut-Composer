# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING
from PyQt5.QtCore import QPoint

if TYPE_CHECKING:
    from ..pie_menu import PieMenu


class PieEditModeHandler:
    """
    Handles the switching between two states of PieMenu action.

    When not in edit mode:
    - PieWidget is shown, PieSettings are not
    - labels cannot be dragged
    - settings button is shown. It allows to enter edit mode

    Wnen in edit mode:
    - Both PieWidget and PieSettings are shown
    - labels can be dragged to, from and inside the PieWidget
    - settings button is replaced with current value icon
    - accept button is shown. It allows to hide everything.

    This class defines what to do, when switching between those states.
    """

    def __init__(self, obj: 'PieMenu') -> None:
        self._is_in_edit_mode = False
        self._obj = obj

    @property
    def is_in_edit_mode(self) -> bool:
        """Return whether the PieMenu is in edit mode"""
        return self._is_in_edit_mode

    def set_edit_mode_true(self) -> None:
        """Set the edit mode on."""
        if self._is_in_edit_mode:
            return

        self._obj.pie_mouse_tracker.stop()

        self._obj.pie_widget.set_draggable(True)
        for widget in self._obj.pie_widget.order_handler.widgets:
            widget.forced = False
        self._obj.pie_widget.active_label = None
        self._obj.pie_widget.repaint()

        self._obj.pie_settings.show()
        self._move_settings_next_to_pie()

        self._obj.accept_button.show()

        self._obj.settings_button.hide()
        self._obj.current_value_holder.show()

        self._is_in_edit_mode = True

    def set_edit_mode_false(self) -> None:
        """Set the edit mode off."""
        if not self._is_in_edit_mode:
            return

        self._obj.pie_widget.hide()
        self._obj.pie_widget.set_draggable(False)

        self._obj.pie_settings.hide()
        self._obj.accept_button.hide()
        self._obj.settings_button.show()
        self._obj.current_value_holder.hide()

        self._is_in_edit_mode = False

    def _move_settings_next_to_pie(self) -> None:
        """Move settings window so that it lies on right side of pie."""
        settings_offset = round(0.5*(
            self._obj.pie_widget.width()
            + self._obj.pie_settings.width()*1.05))

        self._obj.pie_settings.move_center(
            self._obj.pie_widget.center_global
            + QPoint(settings_offset, 0))
