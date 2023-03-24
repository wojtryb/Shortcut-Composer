from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..pie_widget import PieWidget


class EditMode:
    """
    Descriptor that handles the edit mode of PieWidget.

    When red from, it returns a bool telling whether the Pie is in edit mode.
    When mode is changed, changes the Pie's components to reflect that.
    Whe edit mode is turned off, saves the current values to settings.
    """

    def __init__(self) -> None:
        self._edit_mode = False

    def __get__(self, *_) -> bool:
        """Return whether the Pie is in edit mode"""
        return self._edit_mode

    def __set__(self, obj: 'PieWidget', mode_to_set: bool) -> None:
        """Update the mode and change Pie's content accordingly."""
        if not mode_to_set and self._edit_mode:
            self._write_settings(obj)

        self._edit_mode = mode_to_set
        if mode_to_set:
            obj.accept_button.show()
        else:
            obj.accept_button.hide()

    def _write_settings(self, obj: 'PieWidget') -> None:
        """If values were not hardcoded, but from config, write them back."""
        if not obj.labels or obj.config is None:
            return

        values = [widget.label.value for widget in obj.widget_holder]
        obj.config.order.write(values)
