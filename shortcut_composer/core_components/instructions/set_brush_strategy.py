from api_krita import Krita
from api_krita.enums import Tool
from ..instruction_base import Instruction


class SetBrush(Instruction):
    def on_key_press(self) -> None:
        Krita.trigger_action(Tool.FREEHAND_BRUSH.value)


class SetBrushOnNonPaintable(Instruction):
    def on_key_press(self) -> None:
        current_tool = Krita.get_current_tool()
        if not Tool.is_paintable(current_tool):
            Krita.trigger_action(Tool.FREEHAND_BRUSH.value)
