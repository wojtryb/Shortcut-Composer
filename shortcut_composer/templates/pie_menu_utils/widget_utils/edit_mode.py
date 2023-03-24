from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...pie_menu import PieMenu


class EditMode:
    def __init__(self, obj: 'PieMenu') -> None:
        self._edit_mode = False
        self._obj = obj

    def get(self) -> bool:
        """Return whether the Pie is in edit mode"""
        return self._edit_mode

    def set(self, mode_to_set: bool) -> None:
        """Update the mode and change Pie's content accordingly."""
        if not mode_to_set and self._edit_mode:
            self._write_settings()

        if not self._edit_mode ^ mode_to_set:
            return

        if mode_to_set:
            self.set_edit_mode_true()
        else:
            self.set_edit_mode_false()

        self._edit_mode = mode_to_set

    def set_edit_mode_true(self):
        self._obj.pie_widget.set_draggable(True)
        self._obj.pie_widget.is_edit_mode = True
        self._obj.pie_widget.repaint()
        self._obj.pie_settings.show()
        self._obj.accept_button.show()
        self._obj.settings_button.hide()

    def set_edit_mode_false(self):
        self._obj.pie_widget.hide()
        self._obj.pie_widget.set_draggable(False)
        self._obj.pie_widget.is_edit_mode = False
        self._obj.pie_settings.hide()
        self._obj.accept_button.hide()
        self._obj.settings_button.show()
        self._obj.reset()

    def swap_mode(self):
        self.set(not self._edit_mode)

    def _write_settings(self) -> None:
        """If values were not hardcoded, but from config, write them back."""
        widget = self._obj.pie_widget

        if not widget.label_holder or widget.config is None:
            return

        values = [label.value for label in widget.label_holder]
        widget.config.order.write(values)
