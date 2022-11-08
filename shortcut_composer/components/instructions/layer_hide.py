from api_krita import Krita
from ..instruction_base import Instruction


class ToggleLayerVisibility(Instruction):
    def enter(self) -> 'ToggleLayerVisibility':
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
