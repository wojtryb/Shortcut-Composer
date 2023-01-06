from api_krita import Krita
from ..instruction_base import Instruction


class UndoOnShortPress(Instruction):

    def on_short_key_release(self) -> None:
        Krita.trigger_action("edit_undo")
