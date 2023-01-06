# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.wrappers import Database


class Tag(list):
    """
    List-like container representating presets in a tag.

    Created using tag's name, gets filled with preset names.
    Does not update in runtime as the tag gets edited.

    ### Example usage:

    Fetch all brush presets from tag named `Digital`:
    ```python
    Tag("Digital")
    ```
    """

    def __init__(self, name: str) -> None:
        self.name = name
        with Database() as database:
            preset_names = database.get_preset_names_from_tag(name)
        self.extend(set(preset_names))
        self.sort()
