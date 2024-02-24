# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from typing import Tuple, TypeVar
from enum import Enum, EnumMeta

T = TypeVar("T", bound=Enum)


class EnumGroupMeta(EnumMeta):
    """Metaclass for creating enum groups. See EnumGroup documentation."""

    _groups_: dict[str, 'Group']
    """Maps enum groups to their pretty names."""

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs
    ) -> 'EnumGroupMeta':
        # Filter out class attributes provided by Python.
        items: list[Tuple[str, Group]]
        items = [i for i in attrs.items() if not i[0].startswith("__")]

        # Add keys (which will become enum members) to correct groups
        current_group: Group | None = None
        for key, value in items:
            if isinstance(value, Group):
                current_group = value

            elif isinstance(value, (int, str)):
                if current_group is None:
                    raise RuntimeError("Enum defined before first group")
                current_group.keys.append(key)

        # Remove groups from attrs, so they won't become Enum members
        group_var_names = [k for k, v in items if isinstance(v, Group)]
        for group_variable_name in group_var_names:
            members = attrs._member_names
            if sys.version_info.major <= 2:
                raise RuntimeError("Python 2 not supported")
            if sys.version_info.minor <= 10:
                # Until 3.10, _EnumDict._member_names was a list
                members.remove(group_variable_name)
            else:
                # From 3.11, _EnumDict._member_names is a dict
                del members[group_variable_name]

        # Create Enum class. attrs empties itself in a process
        new_class = super().__new__(cls, name, bases, attrs)
        # List of all groups
        group_list = [v for _, v in items if isinstance(v, Group)]

        # Replace keys with their Enum objects, as they exist now
        for group in group_list:
            for key in group.keys:
                group.append(new_class[key])  # type: ignore

        # Store dict mapping groups to their pretty names to use by user
        new_class._groups_ = {group.name: group for group in group_list}

        # Store groups in their respective fields
        for group in group_list:
            setattr(new_class, group.name, group)

        return new_class


class Group(list[Enum]):
    """List of enum members belonging to one Enum."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.keys = []


class EnumGroup(Enum, metaclass=EnumGroupMeta):
    """
    Base class for `Enums` with specified groups.

    Groups are defined by placing separators between the members. Groups
    are lists that will be filled with with the members belonging to it:

    ```python
    class Edible(EnumGroup):
        _fruit = Group("Fruit")
        APPLE = 0
        ORANGE = 1

        _vegetable = Group("Vegetable")
        TOMATO = 2
        POTATO = 3

        def format_member(self):
            return f"{self.name}_{self.value}"
    ```

    Groups can be obtained as attributes, or with `_groups_` dictionary:

    ```python
    assert Edible.APPLE in Edible._fruit
    assert Edible.TOMATO in Edible._groups_["Vegetable"]
    ```

    Groups are class attributes, but they are not Enum members - they
    will not be part of `_member_map_`.

    Every `Enum` member belongs to exactly one group. Every subclass must
    start with a group separator. Otherwise, exception will be raised
    during class creation.
    """
