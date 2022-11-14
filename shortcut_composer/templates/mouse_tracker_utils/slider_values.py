from abc import ABC, abstractmethod
from typing import Iterable, Union, Protocol

from data_components import Range
from .new_types import Interpreted, Controlled


class ListLike(Protocol):
    def index(self, __value: Controlled) -> int: ...
    def __getitem__(self, item: int) -> Controlled: ...
    def __iter__(self) -> Iterable: ...
    def __len__(self) -> int: ...


def create_slider_values(slider_values: Union[ListLike, Range])\
        -> 'SliderValues':
    if isinstance(slider_values, Iterable):
        return ListSliderValues(slider_values)
    elif isinstance(slider_values, Range):
        return RangeSliderValues(slider_values)
    raise RuntimeError(f"Wrong type: {slider_values}")


class SliderValues(ABC):
    
    min: Interpreted
    max: Interpreted
    default: Interpreted

    @abstractmethod
    def at(self, value: Interpreted) -> Controlled: ...

    @abstractmethod
    def index(self, value: Controlled) -> Interpreted: ...


class RangeSliderValues(SliderValues):
    def __init__(self, values: Range):
        self.min = Interpreted(values.min)
        self.max = Interpreted(values.max)
        self.default = Interpreted((self.min + self.max)*0.5)

    def at(self, value: Interpreted) -> Controlled:
        if not self.min <= value <= self.max:
            raise ValueError("Value not in range")
        return Controlled(value)

    def index(self, value: Controlled) -> Interpreted:
        if not self.min <= value <= self.max:
            raise ValueError("Value not in range")
        return Interpreted(value)


class ListSliderValues(SliderValues):
    def __init__(self, values: ListLike):
        self.__values = values
        self.min = Interpreted(-0.49)
        self.default = Interpreted(0)

    @property
    def max(self) -> Interpreted:
        return Interpreted(len(self.__values) - 0.51)

    def at(self, value: Interpreted) -> Controlled:
        return Controlled(self.__values[round(value)])

    def index(self, value: Controlled) -> Interpreted:
        return Interpreted(self.__values.index(value))
