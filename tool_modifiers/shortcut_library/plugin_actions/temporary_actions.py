from dataclasses import dataclass

from .krita_api_wrapper import Krita
from .interfaces import TemporaryAction
from .enums import Tool


@dataclass
class TemporaryTool(TemporaryAction):
    """
    Temporary switches to certain tool. By default goes back to freehand brush.

    action_name: name of action in settings
    krita_tool: tool to switch too
    default_tool (optional): tool to go back to
    time_interval (optional): time after which key press is considered long
    """

    krita_tool: Tool
    default_tool: Tool = Tool.freehand_brush
    time_interval: float = 0.3

    def _set_low(self):
        """Pick a default tool."""
        Krita.trigger_action(self.default_tool.value)

    def _set_high(self):
        """Pick a tool that the action handles."""
        Krita.trigger_action(self.krita_tool.value)

    def _is_high_state(self):
        """Return True when the handled action is active."""
        return Tool(Krita.get_current_tool_name()) == self.krita_tool


@dataclass
class TemporaryEraser(TemporaryAction):
    """
    Temporary switches eraser on.

    action_name (optional): name of action in settings
    affect_preserve_alpha (optional): should toggling turn off preserve_alpha
    time_interval (optional): time after which key press is considered long
    """

    action_name = 'Eraser (toggle)'
    affect_preserve_alpha: bool = True
    time_interval: float = 0.3

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

    action_name: str = 'Preserve alpha (toggle)'
    affect_eraser: bool = True
    time_interval: float = 0.3

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
