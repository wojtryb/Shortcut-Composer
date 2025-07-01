# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar, Iterable

from core_components import Controller
from composer_utils import GroupOrderHolder
from composer_utils.group_manager_impl import dispatch_group_manager
from .pie_config import PieConfig
from .pie_label import PieLabel

T = TypeVar("T")


class PieLabelCreator(Generic[T]):
    """
    Creates PieLabels of single type using passed controller.

    - consist of methods that create PieLabels from different inputs
    - stores known labels in cache to avoid creating them many times
    - allows to fetch list of value groups that can be later used to
      create PieLabels
    """

    known_labels: dict[T, PieLabel[T]] = {}
    """Dictionary of known preset labels mapped to their names."""
    invalid_values: list[T] = []
    """List of values, that are known to result in invalid labels."""

    def __init__(self, controller: Controller[T]) -> None:
        self._controller = controller
        self._group_order_holder = GroupOrderHolder(controller.TYPE)
        self._group_manager = dispatch_group_manager(controller.TYPE)

    def fetch_groups(self) -> list[str]:
        """Return list of value group names."""
        return self._group_manager.fetch_groups()

    def label_from_value(self, value: T | None) -> PieLabel[T] | None:
        """Create single PieLabel from a value. None when impossible."""
        if value is None:
            return None

        if value in self.known_labels:
            return self.known_labels[value]

        if value in self.invalid_values:
            return None

        label = PieLabel.from_value(value, self._controller)
        if label is None:
            self.invalid_values.append(value)
            return None

        return label

    def labels_from_values(
        self,
        values: Iterable[T]
    ) -> list[PieLabel[T]]:
        """Create PieLabels from values. Omit impossible values."""
        labels = [self.label_from_value(value) for value in values]
        return [label for label in labels if label is not None]

    def labels_from_group(
        self,
        group: str,
        sort: bool = True
    ) -> list[PieLabel]:
        """Create PieLabels which values belong to a group."""
        values = self._group_manager.values_from_group(group, sort)
        return self.labels_from_values(values)

    def labels_from_config(self, config: PieConfig) -> list[PieLabel]:
        """Create PieLabels which values are remembered in PieConfig."""
        if not config.GROUP_MODE.read():
            values = config.ORDER.read()
        else:
            group = config.GROUP_NAME.read()
            values = self._group_manager.values_from_group(group)
        return self.labels_from_values(values)
