from typing import Dict, Iterator, Optional

from .label import Label


class LabelHolder:
    def __init__(self):
        self._labels: Dict[int, Label] = {}
        self.active: Optional[Label] = None

    def __setitem__(self, angle: int, label: Label):
        self._labels[angle] = label

    def angles(self):
        return self._labels.keys()

    def __iter__(self) -> Iterator[Label]:
        return iter(self._labels.values())

    def from_angle(self, angle: int) -> Label:
        def angle_difference(label_angle: int):
            raw_difference = label_angle - angle
            return abs((raw_difference + 180) % 360 - 180)

        closest = min(self.angles(), key=angle_difference)
        return self._labels[closest]
