# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Generic, TypeVar
from abc import ABC, abstractmethod

from data_components import Range
from .new_types import Interpreted

Controlled = TypeVar("Controlled")
"""Value compatible with handled controller."""


class SliderValues(ABC, Generic[Controlled]):
    """
    Converts between interpreted values and those compatible with controller.

    Works as if it was a container with  controller compatible values:
    - `at()` fetches controller value using interpreted value
    - `index()` fetches interpreted value using controller value

    Valid interpreted values are a contiguous range - each child of this
    class must contain public attributes:
    - `min` - first valid interpreted value (range beginning)
    - `max` - last valid interpreted value (range end)
    """

    min: Interpreted
    max: Interpreted

    @abstractmethod
    def at(self, value: Interpreted) -> Controlled:
        """Return controller compatible value based on interpreted value."""

    @abstractmethod
    def index(self, value: Controlled) -> Interpreted:
        """Return first occurrence of controlled value."""


class RangeSliderValues(SliderValues):
    """
    Allows to fetch values from Range object defined by the user.

    Moving from interpreted to controller domain require no calculation,
    apart from restricting it to the range `min` and `max` values.
    """

    def __init__(self, values: Range) -> None:
        self.min = Interpreted(values.min)
        self.max = Interpreted(values.max)
        self._default = Interpreted((self.min + self.max)*0.5)

    def at(self, value: Interpreted) -> float:
        """Check if element belongs to the range, and return it as is."""
        if not self.min <= value <= self.max:
            return self._default
        return value

    def index(self, value: float) -> Interpreted:
        """Check if element belongs to the range, and return it as is."""
        if not self.min <= value <= self.max:
            return self._default
        return Interpreted(value)


class ListSliderValues(SliderValues, Generic[Controlled]):
    """
    Allows to fetch values from list or other class with similar interface.

    Unlike in lists, floats are supported for fetching values by
    performing a round() operation.

    `min` and `max` values are provided by analyzing the length of
    controlled list. They represent the full range of values that allow
    to fetch values considering the round conversion.

    Controlled values may change over time.
    """

    def __init__(self, values: list[Controlled]) -> None:
        self._values = values
        self.min = Interpreted(-0.49)

    @property
    def max(self) -> Interpreted:
        """Calculate max as last float, which rounded, returns last element."""
        return Interpreted(len(self._values) - 0.51)

    def at(self, value: Interpreted) -> Controlled:
        """
        Return element of list by rounding input to get list index.

        For values from outside the range, use the right range limit.
        """
        if not self.min <= value <= self.max:
            value = Interpreted(sorted((self.min, value, self.max))[1])
        return self._values[round(value)]

    def index(self, value: Controlled) -> Interpreted:
        """Return index of list element directly from it."""
        if value not in self._values:
            value = self._handle_non_present_element(value)
        return Interpreted(self._values.index(value))

    def _handle_non_present_element(self, value: Controlled) -> Controlled:
        """
        Swap given controlled value, if it does not belong to values list.

        If the handled list elements are not sortable, return first element.
        For sortable elements, snap given value to closest element in a list.
        """
        if not isinstance(value, (int, float)):
            return self._values[0]

        sorted_values: list[Any] = sorted(self._values)
        for list_element in sorted_values:
            if list_element >= value:
                return list_element

        return sorted_values[-1]
