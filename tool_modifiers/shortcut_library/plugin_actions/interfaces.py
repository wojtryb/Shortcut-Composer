from itertools import zip_longest
from typing import Any, List
from dataclasses import dataclass

from .controllers import Controller


@dataclass
class PluginAction:
    """
    Abstract class with custom key event interface

    Child class can specify what to do on any of given callbacks:

    - on_key_press
    - on_short_key_release
    - on_long_key_release
    - on_every_key_release
    """

    action_name: str

    def __pre_init__(self):
        self.time_interval: float

    def on_key_press(self):
        """Called on each press of key specified in settings."""

    def on_long_key_release(self):
        """Called when related key was released after a long time."""

    def on_short_key_release(self):
        """Called when related key was released shortly after press."""

    def on_every_key_release(self):
        """Called on each release of related key, after short/long callback."""


@dataclass
class TemporaryAction(PluginAction):
    """
    Abstract class with custom key event interface for 'temporary keys'

    Action consists of two states: low and high.
    - short key presses toggle between states
    - starting a long press ensures high state
    - ending a long press ensures low state

    Child class has to define both states:
    - set_low
    - set_high
    - is_high_state
    """
    controller: Controller
    high_value: Any
    default_value: Any = None
    time_interval: float = 0.3

    def __post_init__(self):
        if not self.default_value:
            self.default_value = self.controller.default_value

    def _set_low(self) -> None:
        """Defines how to switch to low state."""
        self.controller.set_value(self.default_value)

    def _set_high(self) -> None:
        """Defines how to switch to high state."""
        self.controller.set_value(self.high_value)

    def _is_high_state(self) -> Any:
        """Defines how to determine that current state is high."""
        return self.controller.get_value() == self.high_value

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
class CyclicAction(PluginAction):
    """
    Abstract class with custom key event interface for cyclic actions

    Action cycles around passed 'values_to_cycle':

    - before the cycle starts, long press works as 'temporary key'
    - then, short key press moves to next value.
    - end of long press moves to passed 'default value'

    Child class has to define how to set and determine value:
    - set_value
    - get_current_value
    """
    controller: Controller
    values_to_cycle: List[Any]
    default_value: Any = None
    include_default_in_cycle: bool = False
    time_interval: float = 0.3

    def __post_init__(self):
        """
        Create flag determining that cycling just started.

        If default_value should be taken into consideration, it's simply
        added to the end of cycle list.
        """
        if not self.default_value:
            self.default_value = self.controller.default_value

        self._cycling_just_started: bool = False

        if self.include_default_in_cycle:
            self.values_to_cycle.append(self.default_value)

    def on_key_press(self):
        """Use key press event only for switching to first value."""
        current_value = self.controller.get_value()
        if (
            current_value not in self.values_to_cycle
            or current_value == self.default_value
        ):
            self.controller.set_value(self.values_to_cycle[0])
            self._cycling_just_started = True

    def on_short_key_release(self):
        """Use short press for cycling (apart from starting cycle)"""
        if not self._cycling_just_started:
            self._set_next_value()

    def on_long_key_release(self):
        """All long releases set default value."""
        self.controller.set_value(self.default_value)

    def on_every_key_release(self):
        """Reset flag for 'temporary keys' on first value."""
        self._cycling_just_started = False

    def _set_next_value(self):
        """Move to next value in list. """
        current_value = self.controller.get_value()
        for tool, next_tool in zip_longest(
                self.values_to_cycle,
                self.values_to_cycle[1:],
                fillvalue=self.values_to_cycle[0]):
            if tool == current_value:
                self.controller.set_value(next_tool)
                return
