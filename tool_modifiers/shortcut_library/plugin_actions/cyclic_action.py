from itertools import zip_longest
from typing import Any, List
from dataclasses import dataclass

from ..api_adapter import Controller
from ..plugin_action_utils import PluginAction


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
