from .shortcut_library.plugin_actions.enums import Tools, BlendingModes
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
        krita_tool=Tools.freehand_selection,
    ),
    TemporaryTool(
        action_name="Gradient (toggle)",
        krita_tool=Tools.gradient,
    ),
    TemporaryTool(
        action_name="Line tool (toggle)",
        krita_tool=Tools.line,
    ),
    TemporaryTool(
        action_name="Transform tool (toggle)",
        krita_tool=Tools.transform,
        time_interval=1.0
    ),
    TemporaryTool(
        action_name="Move tool (toggle)",
        krita_tool=Tools.move,
    ),
    CyclicTool(
        action_name="Selections tools (cycle)",
        values_to_cycle=[
            Tools.freehand_selection,
            Tools.rectangular_selection,
            Tools.contiquous_selection,
        ],
    ),
    CyclicTool(
        action_name="Misc tools (cycle)",
        values_to_cycle=[
            Tools.gradient,
            Tools.line,
            Tools.transform,
            Tools.reference,
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
        values_to_cycle=[BlendingModes.overlay],
        include_default_in_cycle=True,
    ),
]
