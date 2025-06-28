# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar, Iterable

from core_components import Controller
from composer_utils import GroupOrderHolder
from .pie_group_manager_impl import dispatch_pie_group_manager
from .pie_widget_utils import PieWidgetLabel
from .pie_config import PieConfig

T = TypeVar("T")


class PieLabelCreator(Generic[T]):

    known_labels: dict[T, PieWidgetLabel[T]] = {}
    """
    Dictionary of known preset labels mapped to their names.

    Allows to avoid creating the same labels multiple times.
    """

    invalid_values: list[T] = []
    """List of preset names, that result in invalid labels."""

    def __init__(self, controller: Controller[T]) -> None:
        self._controller = controller
        self._group_order_holder = GroupOrderHolder(controller.TYPE)
        self._group_manager = dispatch_pie_group_manager(controller)

    def fetch_groups(self) -> list[str]:
        return self._group_manager.fetch_groups()

    def label_from_value(self, value: T | None) -> PieWidgetLabel[T] | None:
        if value is None:
            return None

        if value in self.known_labels:
            return self.known_labels[value]

        if value in self.invalid_values:
            return None

        label = PieWidgetLabel.from_value(value, self._controller)
        if label is None:
            self.invalid_values.append(value)
            return None

        return label

    def labels_from_values(
        self,
        values: Iterable[T]
    ) -> list[PieWidgetLabel[T]]:
        """Create labels from list of preset names."""
        labels = [self.label_from_value(value) for value in values]
        return [label for label in labels if label is not None]

    def labels_from_group(
        self,
        group: str,
        sort: bool = True
    ) -> list[PieWidgetLabel]:
        values = self._group_manager.values_from_group(group, sort)
        return self.labels_from_values(values)

    def labels_from_config(self, config: PieConfig) -> list[PieWidgetLabel]:
        if not config.TAG_MODE.read():
            values = config.ORDER.read()
        else:
            group = config.TAG_NAME.read()
            values = self._group_manager.values_from_group(group)
        return self.labels_from_values(values)
