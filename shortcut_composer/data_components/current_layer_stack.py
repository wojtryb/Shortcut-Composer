from api_krita import Krita
from .pick_strategy import PickStrategy


class CurrentLayerStack(list):
    """
    List-like container which holds nodes currently on layer stack.

    Provides values that can be set with `ActiveLayerController`.
    Is the only list of nodes that can be specified in configuration.

    Is initialized with `PickStrategy`, which can filter layers based on
    their properties (`default: ALL`).

    For more info about avaiable strategies, check `PickStrategy`.

    ### Example usage:
    ```python
    CurrentLayerStack(PickStrategy.CURRENT_VISIBILITY)
    ```
    """

    def __init__(self, pick_strategy: PickStrategy = PickStrategy.ALL) -> None:
        self.pick_strategy = pick_strategy

    def get_layers(self):
        """Use PickStrategy to fetch and filter nodes from the document."""
        if document := Krita.get_active_document():
            return self.pick_strategy.value(document)
        return []

    def __len__(self):
        """HACK: refresh stack here as handler calls it only once on start."""
        self.clear()
        self.extend(self.get_layers())
        return super().__len__()
