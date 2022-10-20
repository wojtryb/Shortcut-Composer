"""File that acts as config - define all action objects here."""

from .shortcut_library.plugin_actions.enums import Tool
from .shortcut_library.plugin_actions import (
    TemporaryEraser,
    TemporaryPreserveAlpha,
    MouseCycleAction,
    TemporaryAction,
    CyclicAction

)
from .shortcut_library.plugin_actions.controllers import (
    BlendingModeController,
    OpacityController,
    PresetController,
    ToolController
)
from .shortcut_library.plugin_actions.handlers import Handler
from .shortcut_library.plugin_actions.helpers import Tag, Range

actions = [
    TemporaryEraser(),
    TemporaryPreserveAlpha(),
    MouseCycleAction(
        action_name="Mouse cycle",
        separate_handlers=False,
        horizontal_handler=Handler(
            controller=OpacityController,
            default_value=0.5,
            values_to_cycle=Range(0.1, 0.9)
            # values_to_cycle=[0.2, 0.3, 0.5, 0.9, 1.0]
        ),
        # horizontal_handler=Handler(
        #     controller=ToolController,
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
            controller=BlendingModeController,
            values_to_cycle=['overlay', 'normal', 'darken'],
            default_value='normal',
            sensitivity=50
        ),
    ),
    TemporaryAction(
        action_name="Freehand selection (toggle)",
        controller=ToolController(),
        high_value=Tool.freehand_selection,
    ),
    TemporaryAction(
        action_name="Gradient (toggle)",
        controller=ToolController(),
        high_value=Tool.gradient,
    ),
    TemporaryAction(
        action_name="Line tool (toggle)",
        controller=ToolController(),
        high_value=Tool.line,
    ),
    TemporaryAction(
        action_name="Transform tool (toggle)",
        controller=ToolController(),
        high_value=Tool.transform,
        time_interval=1.0
    ),
    TemporaryAction(
        action_name="Move tool (toggle)",
        controller=ToolController(),
        high_value=Tool.move,
    ),
    CyclicAction(
        action_name="Selections tools (cycle)",
        controller=ToolController(),
        values_to_cycle=[
            Tool.freehand_selection,
            Tool.rectangular_selection,
            Tool.contiquous_selection,
        ],
    ),
    CyclicAction(
        action_name="Misc tools (cycle)",
        controller=ToolController(),
        values_to_cycle=[
            Tool.gradient,
            Tool.line,
            Tool.transform,
            Tool.reference,
        ],
    ),
    CyclicAction(
        action_name="Preset (cycle)",
        controller=PresetController(),
        default_value="y) Texture Big",
        values_to_cycle=Tag("Digital")
    ),
    CyclicAction(
        action_name="Opacity (cycle)",
        controller=OpacityController(),
        values_to_cycle=[0.75, 0.50],
        include_default_in_cycle=True,
    ),
    CyclicAction(
        action_name="Blending mode (cycle)",
        controller=BlendingModeController(),
        values_to_cycle=["overlay"],
        include_default_in_cycle=True,
    ),
]
