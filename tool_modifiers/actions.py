"""File that acts as config - define all action objects here."""

from .shortcut_library.convenience_utils import Tool
from .shortcut_library.plugin_actions import (
    MouseCycleAction,
    TemporaryAction,
    CyclicAction,
    TemporaryEraser,
    TemporaryPreserveAlpha,
    controllers
)

from .shortcut_library.slider_utils import Handler
from .shortcut_library.convenience_utils import Tag, Range

actions = [
    TemporaryEraser(),
    TemporaryPreserveAlpha(),
    MouseCycleAction(
        action_name="Mouse cycle",
        separate_handlers=True,
        horizontal_handler=Handler(
            controller=controllers.OpacityController,
            default_value=0.5,
            values_to_cycle=Range(0.1, 0.9)
            # values_to_cycle=[0.2, 0.3, 0.5, 0.9, 1.0]
        ),
        # horizontal_handler=Handler(
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
        vertical_handler=Handler(
            controller=controllers.OpacityController,
            default_value=0.5,
            # values_to_cycle=[0.1, 0.2, 0.3, 0.5, 0.9, 1.0]
            values_to_cycle=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        ),
        # vertical_handler=Handler(
        #     controller=controllers.BlendingModeController,
        #     values_to_cycle=['overlay', 'normal', 'darken'],
        #     default_value='normal',
        #     sensitivity=50
        # ),
    ),
    TemporaryAction(
        action_name="Freehand selection (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.freehand_selection,
    ),
    TemporaryAction(
        action_name="Gradient (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.gradient,
    ),
    TemporaryAction(
        action_name="Line tool (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.line,
    ),
    TemporaryAction(
        action_name="Transform tool (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.transform,
        time_interval=1.0
    ),
    TemporaryAction(
        action_name="Move tool (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.move,
    ),
    CyclicAction(
        action_name="Selections tools (cycle)",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.freehand_selection,
            Tool.rectangular_selection,
            Tool.contiquous_selection,
        ],
    ),
    CyclicAction(
        action_name="Misc tools (cycle)",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.gradient,
            Tool.line,
            Tool.transform,
            Tool.reference,
        ],
    ),
    CyclicAction(
        action_name="Preset (cycle)",
        controller=controllers.PresetController(),
        default_value="y) Texture Big",
        values_to_cycle=Tag("Digital")
    ),
    CyclicAction(
        action_name="Opacity (cycle)",
        controller=controllers.OpacityController(),
        values_to_cycle=[0.75, 0.50],
        include_default_in_cycle=True,
    ),
    CyclicAction(
        action_name="Blending mode (cycle)",
        controller=controllers.BlendingModeController(),
        values_to_cycle=["overlay"],
        include_default_in_cycle=True,
    ),
]
