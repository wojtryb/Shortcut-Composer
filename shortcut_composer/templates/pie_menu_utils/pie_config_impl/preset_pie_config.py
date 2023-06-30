# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Callable, Union, Optional
from PyQt5.QtGui import QColor

from config_system import Field
from data_components import Tag, DeadzoneStrategy
from api_krita import Krita
from ..pie_config import PieConfig


class PresetPieConfig(PieConfig[str]):
    """
    FieldGroup representing config of PieMenu of presets.

    Values are calculated according to presets belonging to handled tag
    and the custom order saved by the user in kritarc.
    """

    def __init__(
        self,
        name: str,
        values: Union[Tag, List[str]],
        pie_radius_scale: float,
        icon_radius_scale: float,
        save_local: bool,
        background_color: Optional[QColor],
        active_color: Optional[QColor],
        pie_opacity: int,
        deadzone_strategy: DeadzoneStrategy
    ) -> None:
        super().__init__(name)

        self.PIE_RADIUS_SCALE = self.field("Pie scale", pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field("Icon scale", icon_radius_scale)

        self.SAVE_LOCAL = self.field("Save local", save_local)
        self.DEADZONE_STRATEGY = self.field("deadzone", deadzone_strategy)

        tag_mode = isinstance(values, Tag)
        tag_name = values.tag_name if isinstance(values, Tag) else ""
        self.TAG_MODE = self._create_editable_dual_field("Tag mode", tag_mode)
        self.TAG_NAME = self._create_editable_dual_field("Tag", tag_name)
        self.ORDER = self._create_editable_dual_field("Values", [], str)

        use_default = active_color is None and background_color is None
        if background_color is None:
            background_color = Krita.get_main_color_from_theme()
        if active_color is None:
            active_color = Krita.get_active_color_from_theme()
        self.USE_DEFAULT_THEME = self.field("Use default theme", use_default)
        self.BACKGROUND_COLOR = self.field("Bg color", background_color)
        self.ACTIVE_COLOR = self.field("Active color", active_color)
        self.PIE_OPACITY = self.field("Pie opacity", pie_opacity)

    @property
    def allow_value_edit(self) -> bool:
        """Return whether user can add and remove items from the pie."""
        return not self.TAG_MODE.read()

    def values(self) -> List[str]:
        """Return all presets based on mode and stored order."""
        if not self.TAG_MODE.read():
            return self.ORDER.read()
        return Tag(self.TAG_NAME.read())

    def set_values(self, values: List[str]) -> None:
        """When in tag mode, remember the tag order. Then write normally."""
        if self.TAG_MODE.read():
            group = "ShortcutComposer: Tag order"
            field = Field(group, self.TAG_NAME.read(), [], str)
            field.write(values)

        self.ORDER.write(values)

    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        self.TAG_MODE.field.refresh()
        self.TAG_NAME.field.refresh()
        self.ORDER.write(self.values())

    def set_current_as_default(self):
        """Set current pie values as a new default list of values."""
        self.TAG_MODE.default = self.TAG_MODE.read()
        self.TAG_NAME.default = self.TAG_NAME.read()
        self.ORDER.default = self.ORDER.read()

    def reset_the_default(self) -> None:
        """Set empty pie as a new default list of values."""
        self.TAG_MODE.default = False
        self.TAG_NAME.default = ""
        self.ORDER.default = []

    def reset_to_default(self) -> None:
        """Replace current list of values in pie with the default list."""
        self.TAG_MODE.reset_default()
        self.TAG_NAME.reset_default()
        self.ORDER.reset_default()
        self.refresh_order()

    def is_order_default(self) -> bool:
        """Return whether order is the same as default one."""
        return (
            self.TAG_MODE.read() == self.TAG_MODE.default
            and self.TAG_NAME.read() == self.TAG_NAME.default
            and self.ORDER.read() == self.ORDER.default)

    def register_to_order_related(self, callback: Callable[[], None]) -> None:
        """Register callback to all fields related to value order."""
        self.TAG_MODE.register_callback(callback)
        self.TAG_NAME.register_callback(callback)
        self.ORDER.register_callback(callback)
