from .shortcut_library.plugin_actions import (
    TemporaryTool,
    TemporaryEraser,
    TemporaryAlphaLock,
    CyclicTool,
    CyclicPreset,
    CyclicOpacity,
    CyclicBlendingModes,
)

interval = 0.3
connected_toggles = True
actions = [
    TemporaryEraser(),
    TemporaryAlphaLock(),
    TemporaryTool(
        action_name="Freehand selection (toggle)",
        _krita_tool_name="KisToolSelectOutline",
    ),
    TemporaryTool(
        action_name="Gradient (toggle)",
        _krita_tool_name="KritaFill/KisToolGradient",
    ),
    TemporaryTool(
        action_name="Line tool (toggle)",
        _krita_tool_name="KritaShape/KisToolLine",
    ),
    TemporaryTool(
        action_name="Transform tool (toggle)",
        _krita_tool_name="KisToolTransform",
    ),
    TemporaryTool(
        action_name="Move tool (toggle)",
        _krita_tool_name="KritaTransform/KisToolMove",
    ),
    CyclicTool(
        action_name="Selections tools (cycle)",
        _values_to_cycle=[
            "KisToolSelectOutline",
            "KisToolSelectRectangular",
            "KisToolSelectContiguous",
        ],
    ),
    CyclicTool(
        action_name="Misc tools (cycle)",
        _values_to_cycle=[
            "KritaFill/KisToolGradient",
            "KritaShape/KisToolBrush",
            "KritaShape/KisToolLine",
            "KisToolTransform",
            "ToolReferenceImages",
        ],
    ),
    CyclicPreset(
        action_name="Preset (cycle)",
        _default_value="wojtryb6 R 01 horizontal DA",
        _values_to_cycle=[
            "wojtryb6 R 02a square DA impasto",
            "wojtryb6 R 02b square DA impasto pat",
            "wojtryb6 R 03 square strong impasto",
            "wojtryb6 R 04 square twoSided impasto",
            "wojtryb6 R 05 watercolor",
        ],
    ),
    CyclicOpacity(
        action_name="Opacity (cycle)",
        _default_value=100,
        _values_to_cycle=[75, 50, 100],
    ),
    CyclicBlendingModes(
        action_name="Blending mode (cycle)",
        _values_to_cycle=["overlay", "normal"],
    ),
]
