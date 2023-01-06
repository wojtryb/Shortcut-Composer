# list all the tools you want to create toggles versions

cyclic_tools = {
    "Selections tools (cycle)": [
        "KisToolSelectOutline",
        "KisToolSelectRectangular",
        "KisToolSelectContiguous",
    ],
    "Misc tools (cycle)": [
        "KritaFill/KisToolGradient",
        "KritaShape/KisToolLine",
        "KisToolTransform",
        "ToolReferenceImages",
    ]
}

temporary_tools = {
    "Freehand selection (toggle)": "KisToolSelectOutline",
    "Gradient (toggle)": "KritaFill/KisToolGradient",
    "Line tool (toggle)": "KritaShape/KisToolLine",
    "Transform tool (toggle)": "KisToolTransform",
    "Move tool (toggle)": "KritaTransform/KisToolMove",
}

# time (seconds) after which a press is considered long
interval = 0.3

# using eraser or alpha toggle, resets the other toggle
connected_toggles = True
