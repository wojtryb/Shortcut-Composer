# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar
from PyQt5.QtGui import QColor
from api_krita import Krita
from config_system import FieldGroup
from config_system.field_base_impl import DualField, FieldWithEditableDefault
from data_components import PieDeadzoneStrategy

T = TypeVar("T")
U = TypeVar("U")


class PieConfig(FieldGroup, Generic[T], ABC):
    """Abstract FieldGroup representing config of PieMenu."""

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
        super().__init__(name)
        self._values = values

        self.PIE_RADIUS_SCALE = self.field(
            name="Pie scale",
            default=pie_radius_scale)
        self.ICON_RADIUS_SCALE = self.field(
            name="Icon scale",
            default=icon_radius_scale)

        self.SAVE_LOCAL = self.field(
            name="Save local",
            default=save_local)
        self.DEADZONE_STRATEGY = self.field(
            name="deadzone",
            default=deadzone_strategy)

        override_default = bool(active_color or background_color)
        if background_color is None:
            background_color = Krita.get_main_color_from_theme()
        if active_color is None:
            active_color = Krita.get_active_color_from_theme()

        self.OVERRIDE_DEFAULT_THEME = self.field(
            name="Override default theme",
            default=override_default)
        self.BACKGROUND_COLOR = self.field(
            name="Background color",
            default=background_color)
        self.ACTIVE_COLOR = self.field(
            name="Active color",
            default=active_color)
        self.PIE_OPACITY = self.field(
            name="Pie opacity",
            default=pie_opacity)

    allow_value_edit: bool
    """Is it allowed to remove elements in runtime. """
    name: str
    """Name of field group."""
    ORDER: FieldWithEditableDefault[list[T], DualField[list[T]]]
    """Values displayed in the pie. Used to synchronize pie elements."""

    @abstractmethod
    def values(self) -> list[T]:
        """Return values to display as icons on the pie."""
        ...

    @abstractmethod
    def set_values(self, values: list[T]) -> None:
        """Change current values to new ones."""
        ...

    @abstractmethod
    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        ...

    @abstractmethod
    def set_current_as_default(self) -> None:
        """Set current pie values as a new default list of values."""
        ...

    @abstractmethod
    def reset_the_default(self) -> None:
        """Set empty pie as a new default list of values."""
        ...

    @abstractmethod
    def reset_to_default(self) -> None:
        """Replace current list of values in pie with the default list."""
        ...

    @abstractmethod
    def is_order_default(self) -> bool:
        """Return whether order is the same as default one."""
        ...

    def register_to_order_related(self, callback: Callable[[], None]) -> None:
        """Register callback to all fields related to value order."""
        ...

    def _create_editable_dual_field(
        self,
        field_name: str,
        default: U,
        parser_type: type | None = None
    ) -> FieldWithEditableDefault[U, DualField[U]]:
        """Return field which can switch save location and default value."""
        return FieldWithEditableDefault(
            DualField(self, self.SAVE_LOCAL, field_name, default, parser_type),
            self.field(f"{field_name} default", default, parser_type))
