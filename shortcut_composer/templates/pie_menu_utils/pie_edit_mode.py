# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING
from PyQt5.QtCore import QPoint

if TYPE_CHECKING:
    from ..pie_menu import PieMenu


class PieEditMode:
    """
    Handles the edit mode of the PieMenu action.

    Changing its state to between False and True performs actions on
    PieMenu widgets and components.
    """

    def __init__(self, obj: 'PieMenu') -> None:
        self._edit_mode = False
        self._obj = obj

    def get(self) -> bool:
        """Return whether the Pie is in edit mode"""
        return self._edit_mode

    def set(self, mode_to_set: bool) -> None:
        """Update the mode and change Pie's content accordingly."""
        if not self._edit_mode ^ mode_to_set:
            return

        if mode_to_set:
            self.set_edit_mode_true()
        else:
            self.set_edit_mode_false()
        self._edit_mode = mode_to_set

    def set_edit_mode_true(self) -> None:
        """Set the edit mode on."""
        self._obj.pie_manager.stop(hide=False)
        self._obj.pie_widget.set_draggable(True)
        self._obj.pie_widget.order_handler.widget_holder.clear_forced_widgets()
        self._obj.pie_widget.repaint()
        self._obj.pie_settings.show()
        self._obj.pie_settings.resize(self._obj.pie_settings.sizeHint())
        self._move_settings_next_to_pie()
        self._obj.accept_button.show()
        self._obj.accept_button.move_center(self._obj.pie_widget.center)
        self._obj.settings_button.hide()
        self._obj.pie_widget.active_label = None

    def _move_settings_next_to_pie(self) -> None:
        """Move settings window so that it lies on right side of pie."""
        settings_offset = round(0.5*(
            self._obj.pie_widget.width()
            + self._obj.pie_settings.width()*1.05
        ))
        self._obj.pie_settings.move_center(
            self._obj.pie_widget.center_global
            + QPoint(settings_offset, 0))  # type: ignore

    def set_edit_mode_false(self) -> None:
        """Set the edit mode off."""
        self._obj.pie_widget.hide()
        self._obj.pie_widget.set_draggable(False)
        self._obj.pie_settings.hide()
        self._obj.accept_button.hide()
        self._obj.settings_button.show()

    def swap_mode(self) -> None:
        """Change the edit mode to the other one."""
        self.set(not self._edit_mode)

    def __bool__(self) -> bool:
        return self.get()
