from typing import Any
from ..convenience_utils.helpers import Range


def create_proxy(values_to_cycle, default_value):
    if isinstance(values_to_cycle, list):
        return ListValuesProxy(values_to_cycle, default_value)
    elif isinstance(values_to_cycle, Range):
        return RangeValuesProxy(values_to_cycle, default_value)
    raise RuntimeError(f"Wrong type: {values_to_cycle}")


class ValuesProxy:
    values_to_cycle: Any
    min: float
    max: float
    def at(self, value: float): ...
    def index(self, value: Any): ...


class RangeValuesProxy(ValuesProxy):
    def __init__(self, values_to_cycle: Range, default_value: Any):
        self.values_to_cycle = values_to_cycle
        self.min = values_to_cycle.min
        self.max = values_to_cycle.max
        self.default_value = default_value

    def at(self, value: float):
        return value

    def index(self, value: Any):
        return value


class ListValuesProxy(ValuesProxy):
    def __init__(self, values_to_cycle: list, default_value: Any):
        self.values_to_cycle: list = values_to_cycle
        self.min = -0.49
        self.max = len(values_to_cycle) - 0.51
        self.default_value = values_to_cycle.index(default_value)

    def at(self, value: float):
        return self.values_to_cycle[round(value)]

    def index(self, value: Any):
        return self.values_to_cycle.index(value)
