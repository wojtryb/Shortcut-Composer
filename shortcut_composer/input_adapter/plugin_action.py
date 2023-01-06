from typing import List

from core_components import Controller, InstructionHolder, Instruction


class PluginAction:
    """
    Abstract class with custom key event interface

    Child class can specify what to do on any of given situations:

    - on_key_press
    - on_short_key_release
    - on_long_key_release
    - on_every_key_release
    """

    def __init__(self, *,
                 name: str,
                 time_interval: float = 0.3,
                 controller: Controller = Controller(),
                 instructions: List[Instruction] = []) -> None:
        self.name = name
        self._time_interval = time_interval
        self._controller = controller
        self._instructions = InstructionHolder(instructions)

    def on_key_press(self) -> None:
        """Called on each press of key specified in settings."""

    def on_long_key_release(self) -> None:
        """Called when related key was released after a long time."""

    def on_short_key_release(self) -> None:
        """Called when related key was released shortly after press."""

    def on_every_key_release(self) -> None:
        """Called on each release of related key, after short/long callback."""
