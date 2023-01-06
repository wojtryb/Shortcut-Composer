from dataclasses import dataclass

from ..api_adapter import Krita
from .temporary_action import TemporaryAction


@dataclass
class TemporaryEraser(TemporaryAction):
    """
    Temporary switches eraser on.

    action_name (optional): name of action in settings
    affect_preserve_alpha (optional): should toggling turn off preserve_alpha
    time_interval (optional): time after which key press is considered long
    """

    def __init__(
        self,
        action_name: str = 'Eraser (toggle)',
        affect_preserve_alpha: bool = True,
        time_interval: float = 0.3
    ):
        self.action_name = action_name
        self.affect_preserve_alpha = affect_preserve_alpha
        self.time_interval = time_interval

    def _set_low(self):
        """Turn off the eraser."""
        self._set_eraser(False)

    def _set_high(self):
        """Turn on the eraser."""
        self._set_eraser(True)

    def _is_high_state(self) -> bool:
        """Return True when eraser is on."""
        return Krita.get_action_state("erase_action")

    def _set_eraser(self, state: bool):
        """Set eraser to desired mode, and affect preserve_alpha if needed."""
        if self.affect_preserve_alpha:
            Krita.set_action_state("preserve_alpha", False)
        Krita.set_action_state("erase_action", state)


@dataclass
class TemporaryPreserveAlpha(TemporaryAction):
    """
    Temporary switches preserve_alpha on.

    action_name (optional): name of action in settings
    affect_eraser (optional): should toggling turn off the eraser
    time_interval (optional): time after which key press is considered long
    """

    def __init__(
        self,
        action_name: str = 'Preserve alpha (toggle)',
        affect_eraser: bool = True,
        time_interval: float = 0.3
    ):
        self.action_name = action_name
        self.affect_eraser = affect_eraser
        self.time_interval = time_interval

    def _set_low(self):
        """Turn off preserve_alpha."""
        self._set_preserve_alpha(False)

    def _set_high(self):
        """Turn on preserve_alpha."""
        self._set_preserve_alpha(True)

    def _is_high_state(self) -> bool:
        """Return True when eraser is on."""
        return Krita.get_action_state("preserve_alpha")

    def _set_preserve_alpha(self, state: bool):
        """Set preserve_alpha to desired mode, and affect eraser if needed."""
        if self.affect_eraser:
            Krita.set_action_state("erase_action", False)
        Krita.set_action_state("preserve_alpha", state)
