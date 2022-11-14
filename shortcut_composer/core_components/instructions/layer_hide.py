from api_krita import Krita
from ..instruction_base import Instruction


class ToggleLayerVisibility(Instruction):

    def enter(self) -> 'ToggleLayerVisibility':
        Krita.trigger_action("toggle_layer_visibility")
        return self

    def exit(self, *_) -> None:
        Krita.trigger_action("toggle_layer_visibility")
