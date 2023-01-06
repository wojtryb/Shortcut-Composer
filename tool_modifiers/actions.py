"""File that acts as config - define all action objects here."""

from .shortcut_library.plugin_actions.enums import Tool, BlendingMode
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
        # default_value=Tool.freehand_brush,
        high_value=Tool.freehand_selection,
    ),
    TemporaryAction(
        action_name="Gradient (toggle)",
        controller=ToolController(),
        # default_value=Tool.freehand_brush,
        high_value=Tool.gradient,
    ),
    TemporaryAction(
        action_name="Line tool (toggle)",
        controller=ToolController(),
        # default_value=Tool.freehand_brush,
        high_value=Tool.line,
    ),
    TemporaryAction(
        action_name="Transform tool (toggle)",
        controller=ToolController(),
        # default_value=Tool.freehand_brush,
        high_value=Tool.transform,
        time_interval=1.0
    ),
    TemporaryAction(
        action_name="Move tool (toggle)",
        controller=ToolController(),
        # default_value=Tool.freehand_brush,
        high_value=Tool.move,
    ),
    CyclicAction(
        action_name="Selections tools (cycle)",
        controller=ToolController(),
        # default_value=Tool.freehand_brush,
        values_to_cycle=[
            Tool.freehand_selection,
            Tool.rectangular_selection,
            Tool.contiquous_selection,
        ],
    ),
    CyclicAction(
        action_name="Misc tools (cycle)",
        controller=ToolController(),
        # default_value=Tool.freehand_brush,
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
        default_value="wojtryb6 R 01 horizontal DA",
        values_to_cycle=[
            "wojtryb6 R 02a square DA impasto",
            "wojtryb6 R 02b square DA impasto pat",
            "wojtryb6 R 03 square strong impasto",
            "wojtryb6 R 04 square twoSided impasto",
            "wojtryb6 R 05 watercolor",
        ],
    ),
    CyclicAction(
        action_name="Opacity (cycle)",
        controller=OpacityController(),
        # default_value=1.0,
        values_to_cycle=[0.75, 0.50],
        include_default_in_cycle=True,
    ),
    CyclicAction(
        action_name="Blending mode (cycle)",
        controller=BlendingModeController(),
        # default_value=BlendingMode.normal,
        values_to_cycle=[BlendingMode.overlay],
        include_default_in_cycle=True,
    ),
]
