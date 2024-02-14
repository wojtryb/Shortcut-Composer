# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable, Generic, TypeVar
from PyQt5.QtGui import QColor

from data_components import PieDeadzoneStrategy
from ..pie_config import PieConfig

T = TypeVar("T")


class NonPresetPieConfig(PieConfig[T], Generic[T]):
    """FieldGroup representing config of PieMenu of non-preset values."""

    def __init__(
        self,
        name: str,
        values: list[T],
        pie_radius_scale: float,
        icon_radius_scale: float,
        save_local: bool,
        background_color: QColor | None,
        active_color: QColor | None,
        pie_opacity: int,
        deadzone_strategy: PieDeadzoneStrategy
    ) -> None:
        super().__init__(
            name=name,
            values=values,
            pie_radius_scale=pie_radius_scale,
            icon_radius_scale=icon_radius_scale,
            save_local=save_local,
            background_color=background_color,
            active_color=active_color,
            pie_opacity=pie_opacity,
            deadzone_strategy=deadzone_strategy)

        self.ORDER = self._create_editable_dual_field(
            field_name="Values",
            default=self._values)
        self.allow_value_edit = True

    def values(self) -> list[T]:
        """Return values defined be the user to display as icons."""
        return self.ORDER.read()

    def set_values(self, values: list[T]) -> None:
        """Change current values to new ones."""
        self.ORDER.write(values)

    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        self.ORDER.write(self.values())

    def set_current_as_default(self) -> None:
        """Set current pie values as a new default list of values."""
        self.ORDER.default = self.ORDER.read()

    def reset_the_default(self) -> None:
        """Set empty pie as a new default list of values."""
        self.ORDER.default = []

    def reset_to_default(self) -> None:
        self.ORDER.reset_default()
        self.refresh_order()

    def is_order_default(self) -> bool:
        """Return whether order is the same as default one."""
        return self.ORDER.read() == self.ORDER.default

    def register_to_order_related(self, callback: Callable[[], None]) -> None:
        """Register callback to all fields related to value order."""
        self.ORDER.register_callback(callback)
