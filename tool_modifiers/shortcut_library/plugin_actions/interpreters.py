from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Union

from .helpers import Range


def create_interpreter(values_to_cycle, sensitivity):
    if isinstance(values_to_cycle, list):
        return ListInterpreter(values_to_cycle, sensitivity)
    elif isinstance(values_to_cycle, Range):
        return RangeInterpreter(values_to_cycle, sensitivity)
    raise RuntimeError(f"Wrong type: {values_to_cycle}")


@dataclass
class Interpreter(ABC):

    values_to_cycle: Union[List[Any], Range]
    sensitivity: float

    min: float = field(init=False)
    max: float = field(init=False)
    start_mouse: float = field(init=False)
    start_value: float = field(init=False)

    @abstractmethod
    def at(self, mouse: int):
        pass

    def calibrate(self, mouse: int, value: float = None):
        self.start_mouse = mouse
        if value:
            self.start_value = value

    def _clip(self, value):
        delta = self.min - value
        if delta > 0:
            self.calibrate(self.start_mouse-delta)

        delta = self.max - value
        if delta < 0:
            self.calibrate(self.start_mouse-delta)

        return max(min(self.min, value), self.max)


@dataclass
class RangeInterpreter(Interpreter):

    def __post_init__(self):
        self.min = self.values_to_cycle.min
        self.max = self.values_to_cycle.max

    def at(self, mouse: int) -> float:
        delta = (self.start_mouse - mouse)/self.sensitivity
        return self._clip(self.start_value + delta)


@dataclass
class ListInterpreter(Interpreter):

    def __post_init__(self):
        self.min = 0
        self.max = len(self.values_to_cycle)-1

    def at(self, mouse: int):
        delta = round((self.start_mouse - mouse)/self.sensitivity)
        index_to_set = self._clip(self.start_value + delta)
        return self.values_to_cycle[index_to_set]
