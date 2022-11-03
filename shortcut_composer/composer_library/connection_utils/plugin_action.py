from typing import List, Any
from ..components import Controller, InstructionHolder, Instruction


class PluginAction:
    """
    Abstract class with custom key event interface

    Child class can specify what to do on any of given callbacks:

    - on_key_press
    - on_short_key_release
    - on_long_key_release
    - on_every_key_release
    """

    def __init__(self, *,
                 action_name: str,
                 time_interval: float = 0.3,
                 controller: Controller,
                 additional_instructions: List[Instruction] = []) -> None:
        self.action_name = action_name
        self.time_interval = time_interval
        self.controller = controller
        self.additional_instructions = InstructionHolder(
            additional_instructions)

    def on_key_press(self) -> None:
        """Called on each press of key specified in settings."""

    def on_long_key_release(self) -> None:
        """Called when related key was released after a long time."""

    def on_short_key_release(self) -> None:
        """Called when related key was released shortly after press."""

    def on_every_key_release(self) -> None:
        """Called on each release of related key, after short/long callback."""

    def _read_default_value(self, default_value: Any):
        if default_value:
            return default_value
        return self.controller.default_value
