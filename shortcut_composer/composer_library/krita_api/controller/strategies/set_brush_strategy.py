from enum import Enum

from ...enums import Tool
from ..core_controllers import ToolController


class SetBrushStrategy(Enum):
    @staticmethod
    def __always(): ToolController.set_value(Tool.FREEHAND_BRUSH)

    @staticmethod
    def __never(): ...

    @staticmethod
    def __on_non_paintable():
        current_tool = ToolController.get_value()
        if not Tool.is_paintable(current_tool):
            ToolController.set_value(Tool.FREEHAND_BRUSH)

    ALWAYS = __always
    NEVER = __never
    ON_NON_PAINTABLE = __on_non_paintable
