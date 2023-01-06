from enum import Enum

from ...enums import Tool
from ...core_api import Krita


class SetBrushStrategy(Enum):
    @staticmethod
    def __always() -> None: Krita.trigger_action(Tool.FREEHAND_BRUSH.value)

    @staticmethod
    def __never() -> None: pass

    @staticmethod
    def __on_non_paintable() -> None:
        current_tool = Krita.get_current_tool()
        if not Tool.is_paintable(current_tool):
            Krita.trigger_action(Tool.FREEHAND_BRUSH.value)

    ALWAYS = __always
    NEVER = __never
    ON_NON_PAINTABLE = __on_non_paintable
