from enum import Enum
from composer_utils import Config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..pie_widget import PieWidget


class EditMode:
    def __init__(self) -> None:
        self._edit_mode = False

    def __get__(self, *_):
        return self._edit_mode

    def __set__(self, obj: 'PieWidget', mode_to_set: bool):
        if not mode_to_set and self._edit_mode:
            self._write_settings(obj)

        self._edit_mode = mode_to_set
        if mode_to_set:
            obj.accept_button.show()
        else:
            obj.accept_button.hide()

    def _write_settings(self, obj: 'PieWidget'):
        if not obj.labels or obj._related_config is None:
            return

        values = [widget.label.value for widget in obj.widget_holder]
        if isinstance(values[0], Enum):
            obj._related_config.write(Config.format_enums(values))
        else:
            obj._related_config.write('\t'.join(values))
