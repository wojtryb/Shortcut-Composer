# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from typing import Final, TypeVar, Generic

from PyQt5.QtWidgets import QWidget

from ..field import Field

T = TypeVar("T")


class ConfigBasedWidget(ABC, Generic[T]):
    """
    Wrapper of widget linked to a configuration field.

    The widget is created based on the passed field and available as a
    public attribute.

    Unifies QWidgets interface to `read()` and `set()` methods.
    Additionally, allows to use the configuration field to reset the
    widget to the default value and save current value to config.
    """

    def __init__(
        self,
        config_field: Field,
        parent: QWidget | None,
        pretty_name: str | None,
        tooltip: str | None,
    ) -> None:
        self.config_field: Final[Field] = config_field
        self._parent = parent
        self.pretty_name = self._init_pretty_name(pretty_name)
        self.tooltip = tooltip
        self.widget: QWidget

    @abstractmethod
    def read(self) -> T:
        """Return the current value of the widget."""
        ...

    @abstractmethod
    def set(self, value: T) -> None:
        """Replace the value of the widget with passed one."""
        ...

    def reset(self) -> None:
        """Replace the value of the widget with the default one."""
        self.set(self.config_field.read())

    def save(self) -> None:
        """Save the current value of the widget to kritarc."""
        self.config_field.write(self.read())

    def _init_pretty_name(self, pretty_name: str | None) -> str:
        """Pick the name of the widget. Config field name if not given."""
        if pretty_name is not None:
            return pretty_name
        return self.config_field.name
