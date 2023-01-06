from api_krita import Krita
from .pick_strategy import PickStrategy


class CurrentLayerStack(list):
    def __init__(self, pick_strategy: PickStrategy = PickStrategy.ALL) -> None:
        self.pick_strategy = pick_strategy

    def get_layers(self):
        if document := Krita.get_active_document():
            return self.pick_strategy.value(document)
        return []

    def __len__(self):
        self.clear()
        self.extend(self.get_layers())
        return super().__len__()
