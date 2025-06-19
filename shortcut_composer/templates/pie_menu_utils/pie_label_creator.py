from typing import TypeVar, Generic

from core_components import Controller
from .pie_label import PieLabel

T = TypeVar('T')


class PieLabelCreator(Generic[T]):
    def __init__(self, controller: Controller[T]) -> None:
        self._controller = controller
        self.invalid_values = []

    def create_labels_from_values(self, values: list[T]) -> list[PieLabel[T]]:
        self._controller.refresh()

        labels: list[PieLabel] = []
        for value in values:
            label = PieLabel.from_value(value, self._controller)
            if label is not None:
                labels.append(label)
            else:
                self.invalid_values.append(value)

        return labels

    def filter_values(self, values: list[T]) -> list[T]:
        return [v for v in values if v not in self.invalid_values]
