# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar

from composer_utils import (
    EnumListConfig,
    BuiltinListConfig,
    BuiltinConfig,
    ConfigBase)
from data_components import Tag


T = TypeVar('T')


def create_pie_config(name: str, values: list) -> 'PieConfig':
    if isinstance(values, Tag):
        return PresetPieConfig(name, values)
    return EnumPieConfig(name, values)


class PieConfig:
    name: str
    order: ConfigBase
    values: list


class PresetPieConfig(PieConfig):
    def __init__(self, name: str, tag: Tag) -> None:
        self.name = name
        self.tag_name = BuiltinConfig(name=name, default=tag.tag_name)
        self.order = BuiltinListConfig(f"{self.name} values", [""])

    @property
    def values(self):
        saved_order = self.order.read()
        tag_values = Tag(self.tag_name.read())

        preset_order = [p for p in saved_order if p in tag_values]
        missing = [p for p in tag_values if p not in saved_order]
        return preset_order + missing


class EnumPieConfig(PieConfig):
    def __init__(self, name: str, values: list) -> None:
        self.name = name
        self.order = EnumListConfig(f"{self.name} values", values)

    @property
    def values(self):
        return self.order.read()
