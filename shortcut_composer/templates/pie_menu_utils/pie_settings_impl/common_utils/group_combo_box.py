# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QWidget

from config_system import Field
from config_system.ui import StringComboBox
from .group_manager import GroupManager


class GroupComboBox(StringComboBox):

    def __init__(
        self,
        config_field: Field[str],
        group_fetcher: GroupManager,
        parent: QWidget | None = None,
        pretty_name: str | None = None,
        additional_fields: list[str] = [],
    ) -> None:
        self._additional_fields = additional_fields
        self._group_fetcher = group_fetcher
        super().__init__(config_field, parent, pretty_name)
        self.config_field.register_callback(
            lambda: self.set(self.config_field.read()))

    def reset(self) -> None:
        """Replace list of available tags with those red from database."""
        self._combo_box.clear()
        self._combo_box.addItems(self._additional_fields)
        self._combo_box.addItems(self._group_fetcher.fetch_groups())
        self.set(self.config_field.read())
