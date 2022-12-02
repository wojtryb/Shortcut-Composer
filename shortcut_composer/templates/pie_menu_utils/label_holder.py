from typing import Dict, Iterator

from api_krita.pyqt import Label


class LabelHolder:
    def __init__(self):
        self._labels: Dict[int, Label] = {}

    def __setitem__(self, angle: int, label: Label):
        self._labels[angle] = label

    def angles(self):
        return self._labels.keys()

    def __iter__(self) -> Iterator[Label]:
        return iter(self._labels.values())

    def closest(self, angle: int) -> Label:
        closest = min(self.angles(), key=lambda lab_ang: abs(lab_ang-angle))
        return self._labels[closest]
