"""File that acts as config - define all action objects here."""

from .shortcut_library import plugin_actions as templates
from .shortcut_library.plugin_actions import HideStrategy
from .shortcut_library.api_adapter import controller, Tool, Tag
from .shortcut_library.plugin_actions.slider_utils import Slider, Range

actions = [
    templates.TemporaryEraser(),
    templates.TemporaryPreserveAlpha(),
    templates.LayerPicker(strategy=HideStrategy.MAKE_INVISIBLE),
    templates.VirtualSliderAction(
        action_name="Mouse cycle",
        separate_sliders=True,
        horizontal_slider=Slider(
            controller=controller.OpacityController(),
            default_value=0.5,
            values_to_cycle=Range(0.1, 0.9)
        ),
        vertical_slider=Slider(
            controller=controller.OpacityController(),
            default_value=0.5,
            values_to_cycle=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        ),
        # horizontal_slider=Slider(
        #     controller=controllers.ToolController,
        #     default_value=Tool.freehand_selection,
        #     values_to_cycle=[
        #         Tool.freehand_selection,
        #         Tool.rectangular_selection,
        #         Tool.contiquous_selection,
        #         Tool.gradient,
        #         Tool.line,
        #         Tool.transform,
        #         Tool.reference,
        #     ],
        # ),
        # vertical_slider=Slider(
        #     controller=controllers.BlendingModeController,
        #     values_to_cycle=['overlay', 'normal', 'darken'],
        #     default_value='normal',
        #     sensitivity=50
        # ),
    ),
    templates.TemporaryAction(
        action_name="Freehand selection (toggle)",
        controller=controller.ToolController(),
        high_value=Tool.FREEHAND_SELECTION,
    ),
    templates.TemporaryAction(
        action_name="Gradient (toggle)",
        controller=controller.ToolController(),
        high_value=Tool.GRADIENT,
    ),
    templates.TemporaryAction(
        action_name="Line tool (toggle)",
        controller=controller.ToolController(),
        high_value=Tool.LINE,
    ),
    templates.TemporaryAction(
        action_name="Transform tool (toggle)",
        controller=controller.ToolController(),
        high_value=Tool.TRANSFORM,
        time_interval=1.0
    ),
    templates.TemporaryAction(
        action_name="Move tool (toggle)",
        controller=controller.ToolController(),
        high_value=Tool.MOVE,
    ),
    templates.CyclicAction(
        action_name="Selections tools (cycle)",
        controller=controller.ToolController(),
        values_to_cycle=[
            Tool.FREEHAND_SELECTION,
            Tool.RECTANGULAR_SELECTION,
            Tool.CONTIGUOUS_SELECTION,
        ],
    ),
    templates.CyclicAction(
        action_name="Misc tools (cycle)",
        controller=controller.ToolController(),
        values_to_cycle=[
            Tool.GRADIENT,
            Tool.LINE,
            Tool.TRANSFORM,
            Tool.REFERENCE,
        ],
    ),
    templates.CyclicAction(
        action_name="Preset (cycle)",
        controller=controller.PresetController(),
        default_value="y) Texture Big",
        values_to_cycle=Tag("Digital")
    ),
    templates.CyclicAction(
        action_name="Opacity (cycle)",
        controller=controller.OpacityController(),
        values_to_cycle=[0.75, 0.50],
        include_default_in_cycle=True,
    ),
    templates.CyclicAction(
        action_name="Blending mode (cycle)",
        controller=controller.BlendingModeController(),
        values_to_cycle=["overlay"],
        include_default_in_cycle=True,
    ),
]
