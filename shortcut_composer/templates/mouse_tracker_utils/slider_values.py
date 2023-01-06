from abc import ABC, abstractmethod
from typing import Any, Iterable

from data_components import Range


def create_slider_values(slider_values) -> 'SliderValues':
    if isinstance(slider_values, Iterable):
        return ListSliderValues(slider_values)
    elif isinstance(slider_values, Range):
        return RangeSliderValues(slider_values)
    raise RuntimeError(f"Wrong type: {slider_values}")


class SliderValues(ABC):
    values: Any
    min: float
    max: float
    default_value: float

    @abstractmethod
    def at(self, value: float) -> Any: ...

    @abstractmethod
    def index(self, value: Any) -> Any: ...


class RangeSliderValues(SliderValues):
    def __init__(self, values: Range):
        self.values = values
        self.min = values.min
        self.max = values.max
        self.default_value = (self.min + self.max)*0.5

    def at(self, value: float) -> None:
        return value

    def index(self, value: Any) -> Any:
        if not self.min <= value <= self.max:
            raise ValueError("Value not in range")
        return value


class ListSliderValues(SliderValues):
    def __init__(self, values: list):
        self.slider_values: list = values
        self.min = -0.49
        self.default_value = 0

    @property
    def max(self):
        return len(self.slider_values) - 0.51

    def at(self, value: float) -> Any:
        return self.slider_values[round(value)]

    def index(self, value: Any) -> int:
        return self.slider_values.index(value)
