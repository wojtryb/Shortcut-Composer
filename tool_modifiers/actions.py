"""File that acts as config - define all action objects here."""

from .shortcut_library.plugin_actions.enums import Tool, BlendingMode
from .shortcut_library.plugin_actions import (
    TemporaryTool,
    TemporaryEraser,
    TemporaryAlphaLock,
    CyclicTool,
    CyclicPreset,
    CyclicOpacity,
    CyclicBlendingModes,
)

actions = [
    TemporaryEraser(),
    TemporaryAlphaLock(),
    TemporaryTool(
        action_name="Freehand selection (toggle)",
        krita_tool=Tool.freehand_selection,
    ),
    TemporaryTool(
        action_name="Gradient (toggle)",
        krita_tool=Tool.gradient,
    ),
    TemporaryTool(
        action_name="Line tool (toggle)",
        krita_tool=Tool.line,
    ),
    TemporaryTool(
        action_name="Transform tool (toggle)",
        krita_tool=Tool.transform,
        time_interval=1.0
    ),
    TemporaryTool(
        action_name="Move tool (toggle)",
        krita_tool=Tool.move,
    ),
    CyclicTool(
        action_name="Selections tools (cycle)",
        values_to_cycle=[
            Tool.freehand_selection,
            Tool.rectangular_selection,
            Tool.contiquous_selection,
        ],
    ),
    CyclicTool(
        action_name="Misc tools (cycle)",
        values_to_cycle=[
            Tool.gradient,
            Tool.line,
            Tool.transform,
            Tool.reference,
        ],
    ),
    CyclicPreset(
        action_name="Preset (cycle)",
        default_value="wojtryb6 R 01 horizontal DA",
        values_to_cycle=[
            "wojtryb6 R 02a square DA impasto",
            "wojtryb6 R 02b square DA impasto pat",
            "wojtryb6 R 03 square strong impasto",
            "wojtryb6 R 04 square twoSided impasto",
            "wojtryb6 R 05 watercolor",
        ],
    ),
    CyclicOpacity(
        action_name="Opacity (cycle)",
        default_value=100,
        values_to_cycle=[75, 50],
        include_default_in_cycle=True,
    ),
    CyclicBlendingModes(
        action_name="Blending mode (cycle)",
        values_to_cycle=[BlendingMode.overlay],
        include_default_in_cycle=True,
    ),
]
