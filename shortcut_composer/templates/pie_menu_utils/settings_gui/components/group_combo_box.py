# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from PyQt5.QtWidgets import QWidget

from config_system import Field
from config_system.ui import ConfigComboBox
from .group_fetcher import GroupFetcher


class GroupComboBox(ConfigComboBox):
    """
    Combobox for picking preset tags, which can be saved in config.

    When `allow_all` flag is True, the combobox will contain "All" item
    will be added above the actual tags.
    """

    def __init__(
        self,
        config_field: Field[str],
        group_fetcher: GroupFetcher,
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
        additional_fields: List[str] = [],
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
