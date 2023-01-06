from api_krita import Krita
from ..instruction_base import Instruction


class ToggleLayerVisibility(Instruction):

    def on_key_press(self) -> None:
        self.document = Krita.get_active_document()
        self.affected_node = self.document.active_node
        self.affected_node.toggle_visility()
        self.document.refresh()

    def on_every_key_release(self, *_) -> None:
        self.affected_node.toggle_visility()
        self.document.refresh()


class ToggleShowBelow(Instruction):

    def on_key_press(self) -> None:
        self.document = Krita.get_active_document()
        all_nodes = self.document.get_all_nodes()

        top_nodes = all_nodes[all_nodes.index(self.document.active_node)+1:]
        top_nodes = [node for node in top_nodes if not node.is_group_layer]

        self.visible_nodes = [node for node in top_nodes if node.visible]
        for node in self.visible_nodes:
            node.visible = False

        self.document.refresh()
        return self

    def on_every_key_release(self) -> None:
        for node in self.visible_nodes:
            node.visible = True
        self.document.refresh()
