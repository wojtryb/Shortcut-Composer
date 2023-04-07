# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Generic, TypeVar, Protocol
from config_system import Field, FieldGroup
from data_components import Tag

T = TypeVar("T")


class PieConfig(Protocol, Generic[T]):
    name: str
    values: List[T]
    order: Field[List[T]]
    pie_radius_scale: Field[float]
    icon_radius_scale: Field[float]
    allow_remove: bool


class PresetPieConfig(FieldGroup, PieConfig):
    def __init__(
        self,
        name: str,
        values: Tag,
        pie_radius_scale: float,
        icon_radius_scale: float,
    ) -> None:
        super().__init__(name)
        self.allow_remove = False

        self.pie_radius_scale = self("Pie scale", pie_radius_scale)
        self.icon_radius_scale = self("Icon scale", icon_radius_scale)
        self.tag_name = self("Tag", values.tag_name)
        self.order = self("Values", [""])
        # self.order = self("Values", [], passed_type=str)

    @property
    def values(self) -> List[str]:
        saved_order = self.order.read()
        tag_values = Tag(self.tag_name.read())

        preset_order = [p for p in saved_order if p in tag_values]
        missing = [p for p in tag_values if p not in saved_order]
        return preset_order + missing


class EnumPieConfig(FieldGroup, PieConfig, Generic[T]):
    def __init__(
        self,
        name: str,
        values: List[T],
        pie_radius_scale: float,
        icon_radius_scale: float,
    ) -> None:
        super().__init__(name)
        self.allow_remove = True

        self.pie_radius_scale = self("Pie scale", pie_radius_scale)
        self.icon_radius_scale = self("Icon scale", icon_radius_scale)
        self.order = self("Values", values)

    @property
    def values(self) -> List[T]:
        return self.order.read()
