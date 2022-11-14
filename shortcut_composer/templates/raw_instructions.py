from typing import List, TypeVar

from core_components import Instruction
from input_adapter import PluginAction

T = TypeVar('T')


class RawInstructions(PluginAction):

    def __init__(self, *,
                 action_name: str,
                 instructions: List[Instruction]) -> None:
        super().__init__(
            action_name=action_name,
            instructions=instructions,
            time_interval=0.0)

    def on_key_press(self) -> None:
        """Set high state only if state before press was low."""
        self._instructions.enter()

    def on_every_key_release(self) -> None:
        """End the additional instructions on every key release."""
        self._instructions.exit()
