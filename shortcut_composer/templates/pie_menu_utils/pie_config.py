# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Generic, TypeVar
from config_system import Field, FieldGroup
from data_components import Tag

field = FieldGroup("ShortcutComposer")
T = TypeVar("T")


class PieConfig(Generic[T]):
    values: List[T]
    order: Field
    allow_remove: bool

    def __init__(
        self,
        name: str,
        values: list,
        pie_radius_scale: float,
        icon_radius_scale: float,
    ) -> None:
        self.name = name
        self._default_values = values
        self.pie_radius_scale = field(
            f"{self.name} pie scale",
            pie_radius_scale)
        self.icon_radius_scale = field(
            f"{self.name} icon scale",
            icon_radius_scale)


class PresetPieConfig(PieConfig):
    def __init__(self, *args):
        super().__init__(*args)
        self._default_values: Tag
        self.tag_name = field(self.name, self._default_values.tag_name)
        self.order = field(f"{self.name} values", [""])
        self.allow_remove = False

    @property
    def values(self):
        saved_order = self.order.read()
        tag_values = Tag(self.tag_name.read())

        preset_order = [p for p in saved_order if p in tag_values]
        missing = [p for p in tag_values if p not in saved_order]
        return preset_order + missing


class EnumPieConfig(PieConfig):
    def __init__(self, *args):
        super().__init__(*args)
        self.order = field(f"{self.name} values", self._default_values)
        self.allow_remove = True

    @property
    def values(self):
        return self.order.read()
