from abc import ABC, abstractmethod

from data_components import Range
from .new_types import Interpreted, Controlled


class SliderValues(ABC):
    """
    Interface adapter for values accepted by the slider handler.

    Values are a container with `at()` and `index()` methods.
    Each child class must contain public `min`, `max` and `default`.
    """

    min: Interpreted
    max: Interpreted
    default: Interpreted

    @abstractmethod
    def at(self, value: Interpreted) -> Controlled:
        """Return controller compatibile value based on interpreted value."""

    @abstractmethod
    def index(self, value: Controlled) -> Interpreted:
        """Return first occurance of controlled value."""


class RangeSliderValues(SliderValues):
    """
    Allows to fetch values from user-defined Range.

    Moving from input to output domain require no calculation, apart
    from restricting it to the range `min` and `max` values.
    """

    def __init__(self, values: Range):
        self.min = Interpreted(values.min)
        self.max = Interpreted(values.max)
        self.default = Interpreted((self.min + self.max)*0.5)

    def at(self, value: Interpreted) -> Controlled:
        """Check if element belongs to the range, and return it as is."""
        if not self.min <= value <= self.max:
            raise ValueError("Value not in range")
        return Controlled(value)

    def index(self, value: Controlled) -> Interpreted:
        """Check if element belongs to the range, and return it as is."""
        if not self.min <= value <= self.max:
            raise ValueError("Value not in range")
        return Interpreted(value)


class ListSliderValues(SliderValues):
    """
    Allows to fetch values from list or other class with similar interface.

    Unlike in lists, floats are supported for fetching values by
    performing a round() operation.

    `min` and `max` values are provided by analizing the length of
    controlled list. They represent the full range of values that allow
    to fetch values considering the round conversion.

    Controlled values may change over time.
    """

    def __init__(self, values: list):
        self.__values = values
        self.min = Interpreted(-0.49)
        self.default = Interpreted(0)

    @property
    def max(self) -> Interpreted:
        """Calculate max as last float, which rounded, returns last element."""
        return Interpreted(len(self.__values) - 0.51)

    def at(self, value: Interpreted) -> Controlled:
        """Return element of list by rounding input to get list index."""
        return Controlled(self.__values[round(value)])

    def index(self, value: Controlled) -> Interpreted:
        """Return index of list element directly from it."""
        return Interpreted(self.__values.index(value))
