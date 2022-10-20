from itertools import zip_longest
from typing import Any, List
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PluginAction(ABC):
    """
    Abstract class with custom key event interface

    Child class can specify what to do on any of given callbacks:

    - on_key_press
    - on_short_key_release
    - on_long_key_release
    - on_every_key_release
    """

    action_name: str

    def __post_init__(self):
        self.time_interval: float

    def on_key_press(self):
        """Called on each press of key specified in settings."""

    def on_long_key_release(self):
        """Called when related key was released after a long time."""

    def on_short_key_release(self):
        """Called when related key was released shortly after press."""

    def on_every_key_release(self):
        """Called on each release of related key, after short/long callback."""


class TemporaryAction(PluginAction):
    """
    Abstract class with custom key event interface for 'sticky keys'

    Action consists of two states: low and high.
    - short key presses toggle between states
    - starting a long press ensures high state
    - ending a long press ensures low state

    Child class has to define both states:
    - set_low
    - set_high
    - is_high_state
    """

    @abstractmethod
    def _set_low(self):
        """Defines how to switch to low state."""

    @abstractmethod
    def _set_high(self):
        """Defines how to switch to high state."""

    @abstractmethod
    def _is_high_state(self):
        """Defines how to determine that current state is high."""

    def on_key_press(self):
        """Set high state only if state before press was low."""
        self._state_before_press = self._is_high_state()
        if not self._state_before_press:
            self._set_high()

    def on_short_key_release(self):
        """Set low state only when going from high state."""
        if self._state_before_press:
            self._set_low()

    def on_long_key_release(self):
        """End of long press ensures low state."""
        self._set_low()


@dataclass
class CyclicPluginAction(PluginAction):
    """
    Abstract class with custom key event interface for cyclic actions

    Action cycles around passed 'values_to_cycle':

    - short key moves to next value.
    - when none of the values is active, move to first one
    - end of long press moves to passed 'default value'

    Child class has to define how to set and determine value:
    - set_value
    - get_current_value
    """

    values_to_cycle: List[str]
    default_value: Any

    def __post_init__(self):
        """Create flag that helps to determine state of cycling."""
        self.include_default_in_cycle: bool
        self._wait_for_release: bool = False

        if self.include_default_in_cycle:
            self.values_to_cycle.append(self.default_value)

    @abstractmethod
    def _set_value(self, value: Any) -> None:
        """Defines how to set a passed value."""

    @abstractmethod
    def _get_current_value(self) -> Any:
        """Defines how to determine current value."""

    def on_key_press(self):
        """Use key press event only for switching to first value."""
        current_value = self._get_current_value()
        if (
            current_value not in self.values_to_cycle
            or current_value == self.default_value
        ):
            self._set_value(self.values_to_cycle[0])
            self._wait_for_release = True

    def on_short_key_release(self):
        """Use short press for cycling (apart from starting cycle)"""
        if not self._wait_for_release:
            self._set_next_value()

    def on_long_key_release(self):
        """All long releases set default value."""
        self._set_value(self.default_value)

    def on_every_key_release(self):
        self._wait_for_release = False

    def _set_starting_value(self):
        current_value = self._get_current_value()
        if current_value not in self.values_to_cycle:
            self._set_value(self.values_to_cycle[0])

    def _set_next_value(self):
        current_value = self._get_current_value()
        for tool, next_tool in zip_longest(
                self.values_to_cycle,
                self.values_to_cycle[1:],
                fillvalue=self.values_to_cycle[0]):
            if tool == current_value:
                self._set_value(next_tool)
                return
