from abc import ABC, abstractmethod
from typing import Any, Iterable

from data_components import Range


def create_slider_values(slider_values, default_value) -> 'SliderValues':
    if isinstance(slider_values, Iterable):
        return ListSliderValues(slider_values, default_value)
    elif isinstance(slider_values, Range):
        return RangeSliderValues(slider_values, default_value)
    raise RuntimeError(f"Wrong type: {slider_values}")


class SliderValues(ABC):
    values_to_cycle: Any
    min: float
    max: float

    @abstractmethod
    def at(self, value: float) -> Any: ...

    @abstractmethod
    def index(self, value: Any) -> Any: ...


class RangeSliderValues(SliderValues):
    def __init__(self, slider_values: Range, default_value: float):
        self.values_to_cycle = slider_values
        self.min = slider_values.min
        self.max = slider_values.max
        self.default_value = default_value

    def at(self, value: float) -> None:
        return value

    def index(self, value: Any) -> Any:
        return value


class ListSliderValues(SliderValues):
    def __init__(self, slider_values: list, default_value: Any):
        self.slider_values: list = slider_values
        self.min = -0.49
        self.default_value = self._get_default(default_value)

    @property
    def max(self):
        return len(self.slider_values) - 0.51

    def at(self, value: float) -> Any:
        return self.slider_values[round(value)]

    def index(self, value: Any) -> int:
        return self.slider_values.index(value)

    def _get_default(self, default_value):
        if default_value is not None:
            return self.slider_values.index(default_value)
        return None
