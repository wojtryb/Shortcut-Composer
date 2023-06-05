# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from config_system import Field
from ...pie_style import PieStyle
from .scroll_area import ScrollArea
from ..components import GroupComboBox, GroupFetcher


class GroupScrollArea(ScrollArea):
    def __init__(
        self,
        fetcher: GroupFetcher,
        style: PieStyle,
        columns: int,
        field: Field,
        additional_fields: List[str] = [],
        parent=None
    ) -> None:
        super().__init__(style, columns, parent)
        self._field = field
        self._fetcher = fetcher
        self._chooser = GroupComboBox(
            config_field=self._field,
            group_fetcher=self._fetcher,
            additional_fields=additional_fields)
        self._chooser.widget.currentTextChanged.connect(self._display_group)
        self._layout.insertWidget(0, self._chooser.widget)
        self._display_group()

    def _display_group(self) -> None:
        """Update preset widgets according to tag selected in combobox."""
        picked_group = self._chooser.widget.currentText()
        values = self._fetcher.get_values(picked_group)
        self.replace_handled_labels(self._fetcher.create_labels(values))
        self._apply_search_bar_filter()
        self._chooser.save()
