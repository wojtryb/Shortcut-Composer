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
        free_zone_scale: float,
        divisions: int,
    ) -> None:
        super().__init__(name)

        self.DEADZONE_SCALE = self.field(
            name="Deadzone scale",
            default=deadzone_scale)

        self.FREE_ZONE_SCALE = self.field(
            name="Free zone scale",
            default=free_zone_scale)

        self.DIVISIONS = self.field(
            name="Divisions",
            default=divisions)

    @property
    def deadzone_radius(self) -> int:
        return round(self.DEADZONE_SCALE.read() * 100)

    @property
    def free_zone_radius(self) -> int:
        return round(self.deadzone_radius + self.FREE_ZONE_SCALE.read() * 75)
