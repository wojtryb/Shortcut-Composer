# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol, Generic, TypeVar

T = TypeVar("T")


class GroupManager(Protocol, Generic[T]):
    """
    Interface of class, which reads values that belong to a group.

    While GroupOrderHolder allows to read values saved in previous
    sessions, this GroupManager can get those values from their
    source.

    Accessing different data sources requires different implementations
    of this interface.
    Each type of value requires different class instances.

    It is possible for multiple types of values to have groups with the
    same name.

    Values can be ordered with GroupOrderHolder, but if the group
    changed this class will reflect that:
    - values removed from the group will not be returned even if they
      were present in stored order
    - values added to the group not present in the order, will be
      returned at the end of the list

    """

    def fetch_groups(self) -> list[str]:
        """Return all known groups of handled type of value."""
        ...

    def values_from_group(self, group: str, sort: bool = True) -> list[T]:
        """
        Return all values that belong to the given group.

        If `sort` is True, order from GroupOrderHolder is used.
        Otherwise they will come in the initial order from their source.

        When group is unknown, empty list is returned.

        Use group 'All' to get value from all the groups.
        """
        ...
