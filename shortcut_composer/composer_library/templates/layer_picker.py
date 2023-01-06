from enum import Enum
from typing import List

from ..api import Krita
from ..api.wrappers import Document, Node
from ..components import Instruction, controllers, InstructionHolder
from .mouse_tracker import DoubleAxisTracker
from .slider_utils import Slider, Range


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

    @staticmethod
    def __pick_current_visibility(document: Document) -> List[Node]:
        nodes = document.all_nodes()
        current_node = document.current_node()
        current_visibility = current_node.is_visible()
        return [node for node in nodes
                if node.is_visible() == current_visibility]

    ALL = __pick_all
    VISIBLE = __pick_visible
    CURRENT_VISIBILITY = __pick_current_visibility


class LayerPicker(DoubleAxisTracker):
    def __init__(
        self,
        action_name: str,
        instructions: List[Instruction] = [],
        pick_strategy: PickStrategy = PickStrategy.ALL,
        sensitivity: float = 50.0
    ):
        super().__init__(
            action_name=action_name,
            instructions=InstructionHolder(instructions),
            vertical_slider=Slider(
                controller=controllers.LayerController(),
                values_to_cycle=[0],
                default_value=None,
                sensitivity=sensitivity
            ),
            horizontal_slider=Slider(
                controller=controllers.TimeController(),
                values_to_cycle=Range(1, float('inf')),
                default_value=1,
                sensitivity=sensitivity
            ),
        )
        self.pick_strategy = pick_strategy

    def on_key_press(self) -> None:
        document = Krita.get_active_document()
        self.vertical_slider.set_values_to_cycle(self.pick_strategy(document))
        super().on_key_press()
