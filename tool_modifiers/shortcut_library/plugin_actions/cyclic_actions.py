from dataclasses import dataclass
from typing import List
from krita import Krita

from ._interfaces import CyclicPluginAction
from ._helpers import get_current_tool_name


@dataclass
class CyclicTool(CyclicPluginAction):

    action_name: str
    _values_to_cycle: List[str]
    _default_value: str = "KritaShape/KisToolBrush"

    def _set_value(self, value: str) -> None:
        'activates a tool of passed name'
        Krita.instance().action(value).trigger()

    def _get_current_value(self) -> str:
        return get_current_tool_name()
