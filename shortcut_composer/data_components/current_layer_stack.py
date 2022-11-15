from typing import Any

from api_krita import Krita
from .pick_strategy import PickStrategy


class CurrentLayerStack:
    def __init__(self, pick_strategy: PickStrategy = PickStrategy.ALL) -> None:
        self.pick_strategy = pick_strategy
        self.layers = self.get_layers()

    def get_layers(self):
        if document := Krita.get_active_document():
            return self.pick_strategy.value(document)
        return []

    def __iter__(self):
        return iter(self.layers)

    def __getitem__(self, index: int):
        return self.layers[index]

    def __len__(self):
        self.layers = self.get_layers()
        return len(self.layers)

    def index(self, value: Any):
        return self.layers.index(value)
