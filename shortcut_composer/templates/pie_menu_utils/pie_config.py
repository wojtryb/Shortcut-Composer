# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar, Optional, Union
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

    @abstractmethod
    def set_current_as_default(self) -> None:
        ...

    def _create_editable_dual_field(
        self,
        field_name: str,
        default: U,
        parser_type: Optional[type] = None
    ) -> FieldWithEditableDefault[U, DualField[U]]:
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

    def set_current_as_default(self):
        self.TAG_MODE.default = self.TAG_MODE.read()
        self.TAG_NAME.default = self.TAG_NAME.read()
        self.ORDER.default = self.ORDER.read()


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

    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        self.ORDER.write(self.values())

    def set_current_as_default(self):
        self.ORDER.default = self.ORDER.read()
