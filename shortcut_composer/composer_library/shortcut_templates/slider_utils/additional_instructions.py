from enum import Enum

from ...krita_api import Krita


class AdditionalInstruction:
    def __init__(self): ...
    def __enter__(self): return self
    def update(self) -> None: ...
    def __exit__(self, *_): ...


class HideStrategy(Enum):

    class __IsolateLayerStrategy(AdditionalInstruction):
        def __enter__(self):
            Krita.set_action_state("isolate_active_layer", True)
            return self

        def __exit__(self, *_):
            Krita.set_action_state("isolate_active_layer", False)

    class __MakeInvisibleStrategy(AdditionalInstruction):
        def __init__(self) -> None:
            self.document = Krita.get_active_document()
            self.last_node = self.document.current_node()

        def __enter__(self):
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

        def __exit__(self, *_):
            self.last_node.toggle_visible()
            self.document.refresh()

    NONE = AdditionalInstruction
    ISOLATE_LAYER = __IsolateLayerStrategy
    MAKE_INVISIBLE = __MakeInvisibleStrategy
