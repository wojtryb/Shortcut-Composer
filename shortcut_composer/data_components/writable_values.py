# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from api_krita.wrappers import Database
from composer_utils import Config
from typing import TypeVar
from enum import Enum

T = TypeVar('T', bound=Enum)


class TagConfigValues(list):
    """
    List-based container with preset names fetched from database.

    Created using tag's name stored in passed configuration.
    Uses custom tag order stored in `tag_values` config. All the tag
    values not present in the order will be added to the end.

    Values which are no longer in the tag, will not be included.

    Does not update in runtime as the tag gets edited.

    ### Example usage:

    Fetch all brush presets from tag named stored in TAG_BLUE:
    ```python
    TagConfigValues(Config.TAG_BLUE, Config.TAG_BLUE_VALUES)
    ```
    """

    def __init__(self, tag: Config, tag_values: Config) -> None:
        self.tag = tag
        self.config_to_write = tag_values

        with Database() as database:
            tag_presets = database.get_preset_names_from_tag(tag.read())

        preset_order: List[str] = tag_values.read()
        preset_order = [p for p in preset_order if p in tag_presets]

        missing = [p for p in tag_presets if p not in preset_order]
        self.extend(preset_order + missing)


class EnumConfigValues(list):
    """
    List-based container with enums fetched from configuration.

    ### Example usage:

    Fetch all enums stored in `TRANSFORM_MODES_VALUES` as enum `Tool`:
    ```python
    EnumConfigValues(Config.TRANSFORM_MODES_VALUES, Tool)
    ```
    """

    def __init__(self, values: Config) -> None:
        self.config_to_write = values
        self.extend(values.read())
