from .virtual_slider_action import VirtualSliderAction
from .slider_utils import EmptySlider, Slider
from ..api_adapter import controller, Krita


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

    def on_key_press(self):
        Krita.set_action_state("isolate_active_layer", True)
        nodes = Krita.get_active_document().nodes()
        self.vertical_slider._change_values(nodes)
        super().on_key_press()

    def on_every_key_release(self):
        Krita.set_action_state("isolate_active_layer", False)
        super().on_every_key_release()
