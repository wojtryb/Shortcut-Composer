from ...api import Krita
from ..instruction_base import Instruction


class IsolateLayer(Instruction):
    def enter(self) -> None:
        Krita.set_action_state("isolate_active_layer", True)
        return self

    def exit(self, *_) -> None:
        Krita.set_action_state("isolate_active_layer", False)


class ToggleLayerVisibility(Instruction):
    def enter(self) -> None:
        self.document = Krita.get_active_document()
        self.last_node = self.document.current_node()
        self.last_node.toggle_visible()
        self.document.refresh()
        return self

    def update(self) -> None:
        current_node = self.document.current_node()
        if current_node != self.last_node:
            self.last_node.toggle_visible()
            current_node.toggle_visible()
            self.last_node = current_node
            self.document.refresh()

    def exit(self, *_) -> None:
        self.last_node.toggle_visible()
        self.document.refresh()
