from time import sleep
from typing import Optional

from .virtual_slider_action import VirtualSliderAction
from .slider_utils import EmptySlider, Slider
from ..api_adapter import controller, Krita, Node


class LayerPicker(VirtualSliderAction):
    def __init__(self):
        super().__init__(
            action_name="Layer picker",
            separate_sliders=False,
            horizontal_slider=EmptySlider(),
            vertical_slider=Slider(
                controller=controller.LayerController(),
                values_to_cycle=[0],
                default_value=0,
                sensitivity=50
            ),
        )
        self.working = False
        self.last_node: Optional[Node] = None
        self.document = None

    def on_key_press(self):
        # Krita.set_action_state("isolate_active_layer", True)

        Krita.trigger_action("toggle_layer_visibility")
        self.document = Krita.get_active_document()
        self.last_node = self.document.current_node()

        nodes = self.document.nodes()
        self.vertical_slider._change_values(nodes)
        super().on_key_press()

    def _loop_common(self):
        cursor = Krita.get_cursor()

        self.horizontal_slider.set_start_value(cursor.x)
        self.vertical_slider.set_start_value(-cursor.y)

        self.working = True
        while self.working:
            self.horizontal_slider.handle(cursor.x)
            self.vertical_slider.handle(-cursor.y)

            current_node = self.document.current_node()
            if current_node != self.last_node:
                self.last_node.set_visible(True)
                current_node.set_visible(False)
                self.last_node = current_node
                self.document.refresh()

            sleep(0.05)

    def on_every_key_release(self):
        Krita.trigger_action("toggle_layer_visibility")
        # Krita.set_action_state("isolate_active_layer", False)

        super().on_every_key_release()
