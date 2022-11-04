from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class Range:
    min: float
    max: float


def create_slider_values(values_to_cycle, default_value) -> 'SliderValues':
    if isinstance(values_to_cycle, Iterable):
        return IterableSliderValues(values_to_cycle, default_value)
    elif isinstance(values_to_cycle, Range):
        return RangeSliderValues(values_to_cycle, default_value)
    raise RuntimeError(f"Wrong type: {values_to_cycle}")


class SliderValues(ABC):
    values_to_cycle: Any
    min: float
    max: float

    @abstractmethod
    def at(self, value: float) -> Any: ...

    @abstractmethod
    def index(self, value: Any) -> Any: ...


class RangeSliderValues(SliderValues):
    def __init__(self, values_to_cycle: Range, default_value: float):
        self.values_to_cycle = values_to_cycle
        self.min = values_to_cycle.min
        self.max = values_to_cycle.max
        self.default_value = default_value

    def at(self, value: float) -> None:
        return value

    def index(self, value: Any) -> Any:
        return value


class IterableSliderValues(SliderValues):
    def __init__(self, values_to_cycle: list, default_value: Any):
        self.values_to_cycle: list = values_to_cycle
        self.min = -0.49
        self.default_value = self._get_default(default_value)

    @property
    def max(self):
        return len(self.values_to_cycle) - 0.51

    def at(self, value: float) -> Any:
        return self.values_to_cycle[round(value)]

    def index(self, value: Any) -> int:
        return self.values_to_cycle.index(value)

    def _get_default(self, default_value):
        if default_value is not None:
            return self.values_to_cycle.index(default_value)
        return None
