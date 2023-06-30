# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import List, Callable, Generic, TypeVar, Optional
from PyQt5.QtGui import QColor
from config_system import Field, FieldGroup
from config_system.field_base_impl import DualField, FieldWithEditableDefault
from data_components import DeadzoneStrategy

T = TypeVar("T")
U = TypeVar("U")


class PieConfig(FieldGroup, Generic[T], ABC):
    """Abstract FieldGroup representing config of PieMenu."""

    def __init__(self, name, *args, **kwargs) -> None:
        super().__init__(name)

    allow_value_edit: bool
    """Is it allowed to remove elements in runtime. """

    name: str
    """Name of field group."""

    USE_DEFAULT_THEME: Field[bool]
    BACKGROUND_COLOR: Field[QColor]
    ACTIVE_COLOR: Field[QColor]
    PIE_OPACITY: Field[float]

    SAVE_LOCAL: Field[bool]
    DEADZONE_STRATEGY: Field[DeadzoneStrategy]
    ORDER: FieldWithEditableDefault[List[T], DualField[List[T]]]
    PIE_RADIUS_SCALE: Field[float]
    ICON_RADIUS_SCALE: Field[float]

    @abstractmethod
    def values(self) -> List[T]:
        """Return values to display as icons on the pie."""
        ...

    @abstractmethod
    def set_values(self, values: List[T]) -> None:
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
        parser_type: Optional[type] = None
    ) -> FieldWithEditableDefault[U, DualField[U]]:
        """Return field which can switch save location and default value."""
        return FieldWithEditableDefault(
            DualField(self, self.SAVE_LOCAL, field_name, default, parser_type),
            self.field(f"{field_name} default", default, parser_type))
