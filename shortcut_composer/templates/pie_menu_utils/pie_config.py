# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar, Optional
from PyQt5.QtGui import QColor
from config_system import Field, FieldGroup
from data_components import Tag

T = TypeVar("T")


class PieConfig(FieldGroup, Generic[T], ABC):
    ALLOW_REMOVE: bool

    name: str
    background_color: Optional[QColor]
    active_color: QColor

    ORDER: Field[List[T]]
    PIE_RADIUS_SCALE: Field[float]
    ICON_RADIUS_SCALE: Field[float]

    @abstractmethod
    def values(self) -> List[T]: ...


class PresetPieConfig(PieConfig):

    ALLOW_REMOVE = False

    def __init__(
        self,
        name: str,
        values: Tag,
        pie_radius_scale: float,
        icon_radius_scale: float,
        background_color: Optional[QColor],
        active_color: QColor,
    ) -> None:
        super().__init__(name)

        self.PIE_RADIUS_SCALE = self.field("Pie scale", pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field("Icon scale", icon_radius_scale)
        self.TAG_NAME = self.field("Tag", values.tag_name)
        self.ORDER = self.field("Values", [], passed_type=str)

        self.background_color = background_color
        self.active_color = active_color

    def values(self) -> List[str]:
        saved_order = self.ORDER.read()
        tag_values = Tag(self.TAG_NAME.read())

        preset_order = [p for p in saved_order if p in tag_values]
        missing = [p for p in tag_values if p not in saved_order]
        return preset_order + missing


class EnumPieConfig(PieConfig, Generic[T]):

    ALLOW_REMOVE = True

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

    def values(self) -> List[T]:
        return self.ORDER.read()
