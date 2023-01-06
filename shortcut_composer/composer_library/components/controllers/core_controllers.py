from dataclasses import dataclass

from ...api import Krita
from ...api.wrappers import Node
from ...api.enums import Tool, Toggle
from ..controller_base import Controller


class ToolController(Controller):
    """
    Gives access to tools from toolbox.

    - Operates on `Tool`
    - Defaults to `Tool.FREEHAND_BRUSH`
    """

    default_value: Tool = Tool.FREEHAND_BRUSH

    @staticmethod
    def get_value() -> Tool:
        """Get currently active tool."""
        return Krita.get_current_tool()

    @staticmethod
    def set_value(value: Tool) -> None:
        """Set a passed tool."""
        Krita.trigger_action(value.value)


@dataclass
class ToggleController(Controller):
    """
    Gives access to picked krita toggle action.

    - Pick an action by providing a specific `Toggle`.
    - Operates on booleans
    - Defaults to False
    """

    toggle: Toggle
    default_value = False

    def get_value(self) -> Node:
        return Krita.get_toggle_state(self.toggle)

    def set_value(self, value: bool) -> None:
        Krita.set_toggle_state(self.toggle, value)
