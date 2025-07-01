# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


class Group:
    """
    Wraps a string to mark is as a name of Group.

    For more informations about value Groups in Shortcut Composer read
    dosctrings of GroupManager and GroupOrderHandler in composer_utils.
    """

    def __init__(self, group_name: str) -> None:
        self.group_name = group_name
