# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar, Optional, Union, Callable
from PyQt5.QtGui import QColor
from config_system import Field, FieldGroup
from data_components import Tag

T = TypeVar("T")
F = TypeVar("F", bound=Field)
U = TypeVar("U")


class DualField(Field, Generic[T]):
    """
    Field switching save location based on passed field.

    Implementation uses two identical fields, but with different save
    location. Each time DualField is red or written, correct field is
    picked from the determiner field.

    NOTE: Callbacks are always stored in the global field, as they
    wouldn't run in local one when switching between documents.
    """
    def __new__(cls, *args, **kwargs) -> 'DualField[T]':
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(
        self,
        group: FieldGroup,
        is_local_determiner: Field[bool],
        field_name: str,
        default: T,
        parser_type: Optional[type] = None
    ) -> None:
        self.name = field_name
        self.config_group = group.name
        self.default = default
        self._is_local_determiner = is_local_determiner
        self._is_local_determiner.register_callback(self.refresh)
        self._loc = group.field(field_name, default, parser_type, local=True)
        self._glob = group.field(field_name, default, parser_type, local=False)

    def write(self, value: T) -> None:
        """
        Write to correct internal fields, based on determiner.

        Global field must always be written to activate callbacks.
        """
        if self._is_local_determiner.read():
            self._loc.write(value)
        self._glob.write(value)

    def read(self) -> T:
        """Read from local or global field, based on determiner."""
        if self._is_local_determiner.read():
            return self._loc.read()
        return self._glob.read()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Subscribe callback to both fields, as only one changes on write."""
        self._glob.register_callback(callback)

    def reset_default(self) -> None:
        """Reset both fields to default."""
        self._loc.reset_default()
        self._glob.reset_default()

    def refresh(self) -> None:
        """
        Write red value back to itself.

        Need to be performed manually when active document changes, as it does
        not run callbacks.
        """
        self.write(self.read())


class FieldWithEditableDefault(Field, Generic[T, F]):
    def __new__(cls, *args, **kwargs) -> 'FieldWithEditableDefault[T, F]':
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(self, field: F, field_with_default: Field[T]):
        self.field = field
        self._default_field = field_with_default

        def handle_change_of_default():
            self.field.default = self._default_field.read()
        self._default_field.register_callback(handle_change_of_default)
        handle_change_of_default()

        self.config_group = self.field.config_group
        self.name = self.field.name

    @property
    def default(self) -> T:
        return self.field.default

    @default.setter
    def default(self, value: T) -> None:
        self._default_field.write(value)

    def write(self, value: T) -> None:
        self.field.write(value)

    def read(self) -> T:
        return self.field.read()

    def register_callback(self, callback: Callable[[], None]) -> None:
        self.field.register_callback(callback)

    def reset_default(self) -> None:
        self.field.reset_default()


class PieConfig(FieldGroup, Generic[T], ABC):
    """Abstract FieldGroup representing config of PieMenu."""

    allow_value_edit: bool
    """Is it allowed to remove elements in runtime. """

    name: str
    """Name of field group."""
    background_color: Optional[QColor]
    active_color: QColor

    ORDER: Field[List[T]]
    PIE_RADIUS_SCALE: Field[float]
    ICON_RADIUS_SCALE: Field[float]

    @abstractmethod
    def values(self) -> List[T]:
        """Return values to display as icons on the pie."""
        ...

    @abstractmethod
    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        ...


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

    def _create_editable_dual_field(
        self,
        field_name: str,
        default: U,
        parser_type: Optional[type] = None
    ) -> FieldWithEditableDefault[U, DualField[U]]:
        return FieldWithEditableDefault(
            DualField(self, self.SAVE_LOCAL, field_name, default, parser_type),
            self.field(f"{field_name} default", default, parser_type))

    @property
    def allow_value_edit(self) -> bool:
        """Return whether user can add and remove items from the pie."""
        return not self.TAG_MODE.read()

    def values(self) -> List[str]:
        """Return all presets based on mode and stored order."""
        if not self.TAG_MODE.read():
            return self.ORDER.read()
        saved_order = self.ORDER.read()
        tag_values = Tag(self.TAG_NAME.read())

        preset_order = [p for p in saved_order if p in tag_values]
        missing = [p for p in tag_values if p not in saved_order]
        return preset_order + missing

    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        self.TAG_MODE.field.refresh()
        self.TAG_NAME.field.refresh()
        self.ORDER.write(self.values())


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
        self.ORDER = DualField(self, self.SAVE_LOCAL, "Values", values)

        self.background_color = background_color
        self.active_color = active_color
        self.allow_value_edit = True

    def values(self) -> List[T]:
        """Return values defined be the user to display as icons."""
        return self.ORDER.read()

    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        self.ORDER.write(self.values())
