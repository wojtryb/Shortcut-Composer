# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar

from config_system import FieldGroup

T = TypeVar("T")


class RotationConfig(FieldGroup, Generic[T]):

    def __init__(
        self,
        name: str,
        deadzone_scale: float,
    ) -> None:
        super().__init__(name)

        self.DEADZONE_SCALE = self.field(
            name="Deadzone scale",
            default=deadzone_scale)
