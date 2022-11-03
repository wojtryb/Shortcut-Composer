from ...api import Krita
from ...api.enums import Tool
from ..instruction_base import Instruction


class SetBrush(Instruction):
    def enter(self) -> 'SetBrush':
        Krita.trigger_action(Tool.FREEHAND_BRUSH.value)
        return self


class SetBrushOnNonPaintable(Instruction):
    def enter(self) -> 'SetBrushOnNonPaintable':
        current_tool = Krita.get_current_tool()
        if not Tool.is_paintable(current_tool):
            Krita.trigger_action(Tool.FREEHAND_BRUSH.value)
        return self
