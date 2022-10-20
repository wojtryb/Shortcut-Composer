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
        krita_tool_name="KisToolSelectOutline",
    ),
    TemporaryTool(
        action_name="Gradient (toggle)",
        krita_tool_name="KritaFill/KisToolGradient",
    ),
    TemporaryTool(
        action_name="Line tool (toggle)",
        krita_tool_name="KritaShape/KisToolLine",
    ),
    TemporaryTool(
        action_name="Transform tool (toggle)",
        krita_tool_name="KisToolTransform",
        time_interval=1.0
    ),
    TemporaryTool(
        action_name="Move tool (toggle)",
        krita_tool_name="KritaTransform/KisToolMove",
    ),
    CyclicTool(
        action_name="Selections tools (cycle)",
        values_to_cycle=[
            "KisToolSelectOutline",
            "KisToolSelectRectangular",
            "KisToolSelectContiguous",
        ],
    ),
    CyclicTool(
        action_name="Misc tools (cycle)",
        values_to_cycle=[
            "KritaFill/KisToolGradient",
            "KritaShape/KisToolBrush",
            "KritaShape/KisToolLine",
            "KisToolTransform",
            "ToolReferenceImages",
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
        values_to_cycle=[75, 50, 100],
    ),
    CyclicBlendingModes(
        action_name="Blending mode (cycle)",
        values_to_cycle=["overlay", "normal"],
    ),
]
