# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import abstractmethod
from typing import Final, Optional
from PyQt5.QtWidgets import QWidget

from ..field import Field


class ConfigBasedWidget:
    def __init__(
        self,
        config_field: Field,
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
    ) -> None:
        self._parent = parent
        self.config_field: Final[Field] = config_field
        self.pretty_name = self._init_pretty_name(pretty_name)
        self.widget: QWidget

    @abstractmethod
    def read(self): ...

    @abstractmethod
    def set(self, value): ...

    def reset(self):
        self.set(self.config_field.read())

    def save(self):
        self.config_field.write(self.read())

    def _init_pretty_name(self, pretty_name: Optional[str]) -> str:
        if pretty_name is not None:
            return pretty_name
        return self.config_field.name
