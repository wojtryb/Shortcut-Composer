from api_krita import Krita
from ..instruction_base import Instruction


class ToggleLayerVisibility(Instruction):

    def enter(self) -> 'ToggleLayerVisibility':
        Krita.trigger_action("toggle_layer_visibility")
        return self

    def exit(self, *_) -> None:
        Krita.trigger_action("toggle_layer_visibility")


class ToggleShowBelow(Instruction):

    def enter(self) -> 'ToggleShowBelow':
        self.document = Krita.get_active_document()
        all_nodes = self.document.get_all_nodes()

        top_nodes = all_nodes[all_nodes.index(self.document.active_node)+1:]
        top_nodes = [node for node in top_nodes if not node.is_group_layer]

        self.visible_nodes = [node for node in top_nodes if node.visible]
        for node in self.visible_nodes:
            node.visible = False

        self.document.refresh()
        return self

    def exit(self, *_) -> None:
        for node in self.visible_nodes:
            node.visible = True
        self.document.refresh()
