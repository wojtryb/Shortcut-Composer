from enum import Enum
from time import sleep
from typing import Any, Callable, List, Type, Union


from ..krita_api import Krita, controllers
from ..krita_api.wrappers import Document, Node
from ..krita_api.controllers.base import Controller

from .mouse_tracker import SingleAxisTracker
from .slider_utils import Slider
from .slider_utils.slider_values import Range


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


class LayerPicker(SingleAxisTracker):
    def __init__(
        self,
        action_name: str,
        hide_strategy: HideStrategy = HideStrategy.ISOLATE_LAYER,
        pick_strategy: PickStrategy = PickStrategy.ALL,
        sensitivity: float = 50.0
    ):
        super().__init__(
            action_name=action_name,
            sign=-1,
            slider=HiderSlider(
                controller=controllers.LayerController(),
                values_to_cycle=[0],
                default_value=None,
                hider=hide_strategy.value,
                sensitivity=sensitivity
            ))
        self.hide_strategy = hide_strategy
        self.pick_strategy = pick_strategy

    def on_key_press(self) -> None:
        document = Krita.get_active_document()
        self.slider.set_values_to_cycle(self.pick_strategy(document))
        cursor = Krita.get_cursor()
        return self.slider.start(lambda: self.sign*cursor.y())


class HiderSlider(Slider):
    def __init__(
        self,
        controller: Controller,
        values_to_cycle: Union[List[Any], Range],
        default_value: Any,
        hider: Type[HideStrategy],
        sensitivity: int = 50
    ):
        super().__init__(controller, values_to_cycle, default_value,
                         sensitivity)
        self.hider = hider

    def _loop(self, mouse_getter: Callable[[], int]) -> None:
        document = Krita.get_active_document()
        with self.hider(document) as hider:
            while self._working:
                self._handle(mouse_getter())
                hider.update()
                sleep(0.05)
