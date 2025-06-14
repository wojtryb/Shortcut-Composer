# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterable

from api_krita import Krita
from api_krita.wrappers import Database
from core_components.controllers import PresetController
from data_components import Tag
from ..pie_label import PieLabel
from .group_manager import GroupManager


class PresetGroupManager(GroupManager):
    """TODO"""

    known_labels: dict[str, PieLabel | None] = {}
    """
    Dictionary of known preset labels mapped to their names.

    Allows to avoid creating the same labels multiple times.
    """

    def __init__(self) -> None:
        self._controller = PresetController()

    def fetch_groups(self) -> list[str]:
        with Database() as database:
            return database.get_brush_tags()

    def get_values(self, group: str) -> list[str]:
        if group == "All":
            return list(Krita.get_presets().keys())
        return Tag(group)

    def create_labels(self, values: Iterable[str]) -> list[PieLabel[str]]:
        """Create labels from list of preset names."""
        labels: list[PieLabel | None] = []

        for preset in values:
            if preset in self.known_labels:
                label = self.known_labels[preset]
            else:
                label = PieLabel.from_value(preset, self._controller)
                self.known_labels[preset] = label
            labels.append(label)

        return [label for label in labels if label is not None]
