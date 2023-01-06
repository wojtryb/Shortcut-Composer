from enum import Enum
from time import sleep
from typing import List

from ..krita_api import Krita, controllers
from ..krita_api.wrappers import Document, Node

from .mouse_tracker import MouseTracker
from .slider_utils import EmptySlider, Slider


class HideStrategy(Enum):

    class __HideStrategyBase:
        def __init__(self, _: Document): ...
        def __enter__(self): return self
        def update(self) -> None: ...
        def __exit__(self, *_): ...

    class __IsolateLayerStrategy(__HideStrategyBase):
        def __enter__(self):
            Krita.set_action_state("isolate_active_layer", True)
            return self

        def __exit__(self, *_):
            Krita.set_action_state("isolate_active_layer", False)

    class __MakeInvisibleStrategy(__HideStrategyBase):
        def __init__(self, document: Document) -> None:
            self.document = document
            self.last_node = self.document.current_node()

        def __enter__(self):
            self.last_node.toggle_visible()
            self.document.refresh()
            return self

        def update(self):
            current_node = self.document.current_node()
            if current_node != self.last_node:
                self.last_node.toggle_visible()
                current_node.toggle_visible()
                self.last_node = current_node
                self.document.refresh()

        def __exit__(self, *_):
            self.last_node.toggle_visible()
            self.document.refresh()

    NONE = __HideStrategyBase
    ISOLATE_LAYER = __IsolateLayerStrategy
    MAKE_INVISIBLE = __MakeInvisibleStrategy


class PickStrategy(Enum):
    @staticmethod
    def __pick_all(document: Document) -> List[Node]:
        return document.all_nodes()

    @staticmethod
    def __pick_visible(document: Document) -> List[Node]:
        nodes = document.all_nodes()
        current_node = document.current_node()
        return [node for node in nodes
                if node.is_visible() or node == current_node]

    ALL = __pick_all
    VISIBLE = __pick_visible


class LayerPicker(MouseTracker):
    def __init__(
        self,
        action_name: str,
        hide_strategy: HideStrategy = HideStrategy.ISOLATE_LAYER,
        pick_strategy: PickStrategy = PickStrategy.ALL,
        sensitivity: float = 50.0
    ):
        super().__init__(
            action_name=action_name,
            separate_sliders=False,
            horizontal_slider=EmptySlider(),
            vertical_slider=Slider(
                controller=controllers.LayerController(),
                values_to_cycle=[0],
                default_value=0,
                sensitivity=sensitivity
            ))
        self.hide_strategy = hide_strategy
        self.pick_strategy = pick_strategy

    def _loop_common(self):
        document = Krita.get_active_document()

        with self.hide_strategy.value(document) as hider:
            self.vertical_slider._change_values(self.pick_strategy(document))

            cursor = Krita.get_cursor()
            self.vertical_slider.set_start_value(-cursor.y)

            self.working = True
            while self.working:
                self.vertical_slider.handle(-cursor.y)
                hider.update()
                sleep(0.05)
