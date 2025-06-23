# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterable

from api_krita import Krita
from api_krita.wrappers import Database
from core_components.controllers import PresetController
from data_components import Tag
from ..pie_config import PieConfig
from ..pie_label import PieLabel
from ..group_manager import GroupManager


class PresetGroupManager(GroupManager):
    """TODO"""

    known_labels: dict[str, PieLabel] = {}
    """
    Dictionary of known preset labels mapped to their names.

    Allows to avoid creating the same labels multiple times.
    """

    invalid_presets: list[str] = []
    """List of preset names, that result in invalid labels."""

    def __init__(self) -> None:
        self._controller = PresetController()

    def fetch_groups(self) -> list[str]:
        with Database() as database:
            return database.get_brush_tags()

    def labels_from_values(self, values: Iterable[str]) -> list[PieLabel[str]]:
        """Create labels from list of preset names."""
        labels: list[PieLabel] = []

        for preset in values:
            if preset in self.known_labels:
                labels.append(self.known_labels[preset])
                continue

            if preset in self.invalid_presets:
                continue

            label = PieLabel.from_value(preset, self._controller)
            if label is None:
                self.invalid_presets.append(preset)
                continue

            labels.append(label)

        return labels

    def labels_from_group(self, group: str, sort: bool = True):
        return self.labels_from_values(self._get_values(group, sort))

    def labels_from_config(self, config: PieConfig):
        if not config.TAG_MODE.read():
            values = config.ORDER.read()
        else:
            values = self._get_values(config.TAG_NAME.read())
        return self.labels_from_values(values)

    def _get_values(self, group: str, sort: bool = True) -> list[str]:
        if group == "All":
            return list(Krita.get_presets().keys())
        return Tag(group, sort)
