from itertools import zip_longest
from typing import List
from abc import ABC, abstractmethod


class PluginAction(ABC):

    action_name: str

    def set_low(self):
        pass

    def set_high(self):
        pass

    def is_high_state(self):
        pass


class CyclicPluginAction(PluginAction):

    action_name: str
    values: List[str]
    default_value: str

    @abstractmethod
    def _set_value(self, value: str) -> None:
        pass

    @abstractmethod
    def _get_current_value(self) -> str:
        pass

    def set_low(self):
        self._set_value(self.default_value)

    def set_high(self):
        current_value = self._get_current_value()
        if current_value not in self.values:
            self._set_value(self.values[0])
            return

        for tool, next_tool in zip_longest(
                self.values,
                self.values[1:],
                fillvalue=self.values[0]):
            if tool == current_value:
                self._set_value(next_tool)
                return

    def is_high_state(self):
        return False
