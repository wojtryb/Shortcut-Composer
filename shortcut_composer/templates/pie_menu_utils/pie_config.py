# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar, Optional
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


class PresetPieConfig(PieConfig[str]):
    """
    FieldGroup representing config of PieMenu of presets.

    Values are calculated according to presets belonging to handled tag
    and the custom order saved by the user in kritarc.
    """

    def __init__(
        self,
        name: str,
        values: Tag,
        pie_radius_scale: float,
        icon_radius_scale: float,
        background_color: Optional[QColor],
        active_color: QColor,
        is_tag_mode: bool,
    ) -> None:
        super().__init__(name)

        self.PIE_RADIUS_SCALE = self.field("Pie scale", pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field("Icon scale", icon_radius_scale)
        self.TAG_NAME = self.field("Tag", values.tag_name)
        self.ORDER = self.field("Values", [], parser_type=str)
        self.IS_TAG_MODE = self.field("Is tag mode", is_tag_mode)

        self.background_color = background_color
        self.active_color = active_color

    @property
    def allow_value_edit(self):
        """Return whether user can add and remove items from the pie."""
        return not self.IS_TAG_MODE.read()

    def values(self) -> List[str]:
        """Return all presets from the tag. Respect order from kritarc."""
        if not self.IS_TAG_MODE.read():
            return self.ORDER.read()
        saved_order = self.ORDER.read()
        tag_values = Tag(self.TAG_NAME.read())

        preset_order = [p for p in saved_order if p in tag_values]
        missing = [p for p in tag_values if p not in saved_order]
        return preset_order + missing

    def refresh_order(self):
        """Write current list of values to order field."""
        self.ORDER.write(self.values())


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
