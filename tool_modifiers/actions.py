"""File that acts as config - define all action objects here."""

from .shortcut_library.plugin_actions.enums import Tool
from .shortcut_library.plugin_actions import (
    TemporaryEraser,
    TemporaryPreserveAlpha,
    MouseCycle,
    TemporaryAction,
    CyclicAction

)
from .shortcut_library.plugin_actions.controllers import (
    BlendingModeController,
    OpacityController,
    PresetController,
    ToolController
)
from .shortcut_library.plugin_actions.mouse_cycle import Handler
from .shortcut_library.plugin_actions.helpers import Tag

actions = [
    TemporaryEraser(),
    TemporaryPreserveAlpha(),
    MouseCycle(
        action_name="Mouse cycle",
        horizontal_handler=Handler(),
        vertical_handler=Handler(),
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
