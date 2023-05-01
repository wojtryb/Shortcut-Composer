# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar, Optional, Union, Callable
from PyQt5.QtGui import QColor
from config_system import Field, FieldGroup
from data_components import Tag

T = TypeVar("T")


class PieConfig(FieldGroup, Generic[T], ABC):
    """Abstract FieldGroup representing config of PieMenu."""

    allow_value_edit: bool
    """Is it allowed to remove elements in runtime. """

    name: str
    """Name of the group in kritarc."""
    background_color: Optional[QColor]
    active_color: QColor

    ORDER: Field[List[T]]
    """Value order stored in kritarc."""
    PIE_RADIUS_SCALE: Field[float]
    ICON_RADIUS_SCALE: Field[float]

    @abstractmethod
    def values(self) -> List[T]:
        """Return values to display as icons on the pie."""
        ...

    @abstractmethod
    def set_values(self, values: List[T]) -> None:
        ...


class DualField(Field, Generic[T]):
    def __new__(cls, *args, **kwargs) -> 'DualField[T]':
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(
        self,
        group: PieConfig,
        is_local_determiner: Field[bool],
        field_name: str,
        default: T,
        parser_type: Optional[type] = None
    ) -> None:
        self.name = field_name
        self.config_group = group.name
        self.default = default
        self._is_local_determiner = is_local_determiner
        self._loc = group.field(field_name, default, parser_type, local=True)
        self._glob = group.field(field_name, default, parser_type, local=False)

    def write(self, value: T):
        if self._is_local_determiner.read():
            self._loc.write(value)
        self._glob.write(value)

    def read(self) -> T:
        if self._is_local_determiner.read():
            return self._loc.read()
        return self._glob.read()

    def register_callback(self, callback: Callable[[], None]):
        self._glob.register_callback(callback)

    def reset_default(self) -> None:
        self._glob.reset_default()
        self._loc.reset_default()


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
        background_color: Optional[QColor],
        active_color: QColor,
        tag_mode: bool,
    ) -> None:
        super().__init__(name)
        tag_name = values.tag_name if isinstance(values, Tag) else ""

        self.PIE_RADIUS_SCALE = self.field("Pie scale", pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field("Icon scale", icon_radius_scale)

        self.IS_LOCAL = self.field("Is local", True)

        self.TAG_NAME = DualField(self, self.IS_LOCAL, "Tag", tag_name)
        self.ORDER = DualField(self, self.IS_LOCAL, "Values", [], str)
        self.TAG_MODE = DualField(self, self.IS_LOCAL, "Is tag mode", tag_mode)

        self.background_color = background_color
        self.active_color = active_color

    @property
    def allow_value_edit(self):
        """Return whether user can add and remove items from the pie."""
        return not self.TAG_MODE.read()

    def values(self) -> List[str]:
        """Return all presets from the tag. Respect order from kritarc."""
        if not self.TAG_MODE.read():
            return self.ORDER.read()
        saved_order = self.ORDER.read()
        tag_values = Tag(self.TAG_NAME.read())

        preset_order = [p for p in saved_order if p in tag_values]
        missing = [p for p in tag_values if p not in saved_order]
        return preset_order + missing

    def set_values(self, values: List[str]):
        self.TAG_MODE.write(self.TAG_MODE.read())
        self.TAG_NAME.write(self.TAG_NAME.read())
        self.ORDER.write(values)

    def refresh_order(self):
        """Write current list of values to order field."""
        self.set_values(self.values())


class NonPresetPieConfig(PieConfig[T], Generic[T]):
    """FieldGroup representing config of PieMenu of non-preset values."""

    def __init__(
        self,
        name: str,
        values: List[T],
        pie_radius_scale: float,
        icon_radius_scale: float,
        background_color: Optional[QColor],
        active_color: QColor,
    ) -> None:
        super().__init__(name)

        self.PIE_RADIUS_SCALE = self.field("Pie scale", pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field("Icon scale", icon_radius_scale)
        self.ORDER = self.field("Values", values)

        self.background_color = background_color
        self.active_color = active_color
        self.allow_value_edit = True

    def values(self) -> List[T]:
        """Return values to display as icons as defined be the user."""
        return self.ORDER.read()

    def set_values(self, values: List[T]):
        self.ORDER.write(values)
