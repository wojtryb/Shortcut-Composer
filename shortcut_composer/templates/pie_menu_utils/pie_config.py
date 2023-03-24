# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from composer_utils import (
    EnumListConfig,
    BuiltinListConfig,
    BuiltinConfig,
    ConfigBase)
from data_components import Tag


def create_pie_config(
    name: str,
    values: list,
    pie_radius_scale: float,
    icon_radius_scale: float,
) -> 'PieConfig':
    args = [name, values, pie_radius_scale, icon_radius_scale]
    if isinstance(values, Tag):
        return PresetPieConfig(*args)
    return EnumPieConfig(*args)


class PieConfig:
    values: list
    order: ConfigBase

    def __init__(
        self,
        name: str,
        values: list,
        pie_radius_scale: float,
        icon_radius_scale: float,
    ) -> None:
        self.name = name
        self._default_values = values
        self.pie_radius_scale = BuiltinConfig(
            f"{self.name} pie scale",
            pie_radius_scale)
        self.icon_radius_scale = BuiltinConfig(
            f"{self.name} icon scale",
            icon_radius_scale)


class PresetPieConfig(PieConfig):
    def __init__(self, *args):
        super().__init__(*args)
        self._default_values: Tag
        self.tag_name = BuiltinConfig(self.name, self._default_values.tag_name)
        self.order = BuiltinListConfig(f"{self.name} values", [""])

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
        self.order = EnumListConfig(
            f"{self.name} values",
            self._default_values)

    @property
    def values(self):
        return self.order.read()
