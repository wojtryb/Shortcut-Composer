# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Callable, Generic, TypeVar, Optional, Union
from PyQt5.QtGui import QColor
from config_system import Field, FieldGroup
from config_system.fields import DualField, FieldWithEditableDefault
from data_components import Tag

T = TypeVar("T")
U = TypeVar("U")


class PieConfig(FieldGroup, Generic[T], ABC):
    """Abstract FieldGroup representing config of PieMenu."""

    allow_value_edit: bool
    """Is it allowed to remove elements in runtime. """

    name: str
    """Name of field group."""
    background_color: Optional[QColor]
    active_color: QColor

    SAVE_LOCAL: Field[bool]
    ORDER: FieldWithEditableDefault[List[T], DualField[List[T]]]
    PIE_RADIUS_SCALE: Field[float]
    ICON_RADIUS_SCALE: Field[float]

    @abstractmethod
    def values(self) -> List[T]:
        """Return values to display as icons on the pie."""
        ...

    @abstractmethod
    def set_values(self, values: List[T]) -> None:
        """Change current values to new ones."""
        ...

    @abstractmethod
    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        ...

    @abstractmethod
    def set_current_as_default(self) -> None:
        """Set current pie values as a new default list of values."""
        ...

    @abstractmethod
    def reset_the_default(self) -> None:
        """Set empty pie as a new default list of values."""
        ...

    @abstractmethod
    def reset_to_default(self) -> None:
        """Replace current list of values in pie with the default list."""
        ...

    @abstractmethod
    def is_order_default(self) -> bool:
        """Return whether order is the same as default one."""
        ...

    def register_to_order_related(self, callback: Callable[[], None]) -> None:
        """Register callback to all fields related to value order."""
        ...

    def _create_editable_dual_field(
        self,
        field_name: str,
        default: U,
        parser_type: Optional[type] = None
    ) -> FieldWithEditableDefault[U, DualField[U]]:
        """Return field which can switch save location and default value."""
        return FieldWithEditableDefault(
            DualField(self, self.SAVE_LOCAL, field_name, default, parser_type),
            self.field(f"{field_name} default", default, parser_type))


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
        active_color: QColor,
    ) -> None:
        super().__init__(name)

        self.PIE_RADIUS_SCALE = self.field("Pie scale", pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field("Icon scale", icon_radius_scale)

        self.SAVE_LOCAL = self.field("Save local", save_local)

        tag_mode = isinstance(values, Tag)
        tag_name = values.tag_name if isinstance(values, Tag) else ""
        self.TAG_MODE = self._create_editable_dual_field("Tag mode", tag_mode)
        self.TAG_NAME = self._create_editable_dual_field("Tag", tag_name)
        self.ORDER = self._create_editable_dual_field("Values", [], str)

        self.background_color = background_color
        self.active_color = active_color

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


class NonPresetPieConfig(PieConfig[T], Generic[T]):
    """FieldGroup representing config of PieMenu of non-preset values."""

    def __init__(
        self,
        name: str,
        values: List[T],
        pie_radius_scale: float,
        icon_radius_scale: float,
        save_local: bool,
        background_color: Optional[QColor],
        active_color: QColor,
    ) -> None:
        super().__init__(name)

        self.PIE_RADIUS_SCALE = self.field("Pie scale", pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field("Icon scale", icon_radius_scale)

        self.SAVE_LOCAL = self.field("Save local", save_local)
        self.ORDER = self._create_editable_dual_field("Values", values)

        self.background_color = background_color
        self.active_color = active_color
        self.allow_value_edit = True

    def values(self) -> List[T]:
        """Return values defined be the user to display as icons."""
        return self.ORDER.read()

    def set_values(self, values: List[T]) -> None:
        """Change current values to new ones."""
        self.ORDER.write(values)

    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        self.ORDER.write(self.values())

    def set_current_as_default(self):
        """Set current pie values as a new default list of values."""
        self.ORDER.default = self.ORDER.read()

    def reset_the_default(self) -> None:
        """Set empty pie as a new default list of values."""
        self.ORDER.default = []

    def reset_to_default(self) -> None:
        self.ORDER.reset_default()
        self.refresh_order()

    def is_order_default(self) -> bool:
        """Return whether order is the same as default one."""
        return self.ORDER.read() == self.ORDER.default

    def register_to_order_related(self, callback: Callable[[], None]) -> None:
        """Register callback to all fields related to value order."""
        self.ORDER.register_callback(callback)
