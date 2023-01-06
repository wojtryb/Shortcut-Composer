from itertools import zip_longest
from typing import List
from abc import ABC, abstractmethod
from dataclasses import field


class PluginAction(ABC):

    action_name: str

    def on_key_press(self):
        pass

    def on_long_key_release(self):
        pass

    def on_short_key_release(self):
        pass

    def on_every_key_release(self):
        pass


class TemporaryAction(PluginAction):

    action_name: str

    @abstractmethod
    def _set_low(self):
        pass

    @abstractmethod
    def _set_high(self):
        pass

    @abstractmethod
    def _is_high_state(self):
        pass

    def on_key_press(self):
        self._state_before_press = self._is_high_state()
        if not self._state_before_press:
            self._set_high()

    def on_short_key_release(self):
        if self._state_before_press:
            self._set_low()

    def on_long_key_release(self):
        self._set_low()


class CyclicPluginAction(PluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str

    _wait_for_release = field(default=False, init=False)

    @abstractmethod
    def _set_value(self, value: str) -> None:
        pass

    @abstractmethod
    def _get_current_value(self) -> str:
        pass

    def on_key_press(self):
        current_value = self._get_current_value()
        if current_value not in self._values_to_cycle:
            self._set_value(self._values_to_cycle[0])
            self._wait_for_release = True
            return

        if current_value == self._default_value:
            self._set_value(self._values_to_cycle[0])
            self._wait_for_release = True

    def on_short_key_release(self):
        if not self._wait_for_release:
            self._set_next_value()

    def on_long_key_release(self):
        self._set_value(self._default_value)

    def on_every_key_release(self):
        self._wait_for_release = False

    def _set_starting_value(self):
        current_value = self._get_current_value()
        if current_value not in self._values_to_cycle:
            self._set_value(self._values_to_cycle[0])

    def _set_next_value(self):
        current_value = self._get_current_value()
        for tool, next_tool in zip_longest(
                self._values_to_cycle,
                self._values_to_cycle[1:],
                fillvalue=self._values_to_cycle[0]):
            if tool == current_value:
                self._set_value(next_tool)
                return
