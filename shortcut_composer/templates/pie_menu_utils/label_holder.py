# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Iterator, Optional

from .label import Label


class LabelHolder:
    """
    Holds Labels and allows fetching them using their angle.

    Allows one of the labels to be active, but does not handle this
    attribute by itself.

    Allows iterating over Labels (default) and over angles (angles())
    """

    def __init__(self):
        self._labels: Dict[int, Label] = {}
        self.active: Optional[Label] = None

    def add(self, label: Label) -> None:
        """Add a new label to the holder."""
        self._labels[label.angle] = label

    def angles(self) -> Iterator[int]:
        """Iterate over all angles of held Labels."""
        return iter(self._labels.keys())

    def from_angle(self, angle: int) -> Label:
        """Return Label which is the closest to given `angle`."""

        def angle_difference(label_angle: int):
            """Return the smallest difference between two angles."""
            nonlocal angle
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self.angles(), key=angle_difference)
        return self._labels[closest]

    def __iter__(self) -> Iterator[Label]:
        """Iterate over all held labels."""
        return iter(self._labels.values())

    def __len__(self) -> int:
        """Return amount of held labels."""
        return len(self._labels)
