"""
Implementation of all plugin actions.

Remember to define every action under exactly the same name in the
`shortcut_composer.action` file. Otherwise the action will not be
visible in `keyboard shortcuts` menu in krita settings.
"""

import templates
from api_krita.enums import BlendingMode, Tool, Toggle
from core_components import instructions, controllers
from data_components import (
    CurrentLayerStack,
    PickStrategy,
    Slider,
    Range,
    Tag,
)


actions = [
    templates.TemporaryKey(
        name="Temporary move tool",
        controller=controllers.ToolController(),
        high_value=Tool.MOVE,
    ),
    templates.TemporaryKey(
        name="Temporary transform tool",
        controller=controllers.ToolController(),
        high_value=Tool.TRANSFORM,
        time_interval=1.0
    ),
    templates.TemporaryKey(
        name="Temporary eraser",
        controller=controllers.ToggleController(Toggle.ERASER),
        low_value=False,
        high_value=True,
        instructions=[
            instructions.SetBrushOnNonPaintable(),
            instructions.EnsureOff(Toggle.PRESERVE_ALPHA),
        ],
    ),
    templates.TemporaryKey(
        name="Temporary preserve alpha",
        controller=controllers.ToggleController(Toggle.PRESERVE_ALPHA),
        low_value=False,
        high_value=True,
        instructions=[
            instructions.SetBrushOnNonPaintable(),
            instructions.EnsureOff(Toggle.ERASER),
        ],
    ),
    templates.RawInstructions(
        name="Preview current layer visibility",
        instructions=[instructions.ToggleLayerVisibility()],
    ),
    templates.RawInstructions(
        name="Preview projection below",
        instructions=[instructions.ToggleShowBelow()],
    ),
    templates.MultipleAssignment(
        name="Cycle painting opacity",
        controller=controllers.OpacityController(),
        default_value=100,
        values_to_cycle=[70, 50, 30, 100],
    ),
    templates.MultipleAssignment(
        name="Cycle selection tools",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.FREEHAND_SELECTION,
            Tool.RECTANGULAR_SELECTION,
            Tool.CONTIGUOUS_SELECTION,
        ],
    ),
    templates.MultipleAssignment(
        name="Cycle misc tools",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.CROP,
            Tool.REFERENCE,
            Tool.GRADIENT,
            Tool.MULTI_BRUSH,
        ],
    ),
    templates.MultipleAssignment(
        name="Cycle painting blending modes",
        controller=controllers.BlendingModeController(),
        values_to_cycle=[
            BlendingMode.OVERLAY,
            BlendingMode.MULTIPLY,
            BlendingMode.COLOR,
            BlendingMode.ADD,
            BlendingMode.BEHIND,
            BlendingMode.DARKEN,
            BlendingMode.LIGHTEN,
            BlendingMode.NORMAL,
        ],
    ),
    templates.MultipleAssignment(
        name="Cycle brush presets",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        values_to_cycle=Tag("Digital"),
        default_value="b) Basic-5 Size Opacity",
    ),
    templates.MouseTracker(
        name="Scroll undo stack",
        instructions=[instructions.UndoOnShortPress()],
        horizontal_slider=Slider(
            controller=controllers.UndoController(),
            values=Range(float('-inf'), float('inf')),
            deadzone=100,
        )
    ),
    templates.MouseTracker(
        name="Scroll isolated layers",
        instructions=[instructions.TemporaryOn(Toggle.ISOLATE_LAYER)],
        vertical_slider=Slider(
            controller=controllers.LayerController(),
            values=CurrentLayerStack(PickStrategy.ALL),
        )
    ),
    templates.MouseTracker(
        name="Scroll timeline or animated layers",
        instructions=[instructions.TemporaryOn(Toggle.ISOLATE_LAYER)],
        horizontal_slider=Slider(
            controller=controllers.TimeController(),
            values=Range(0, float('inf')),
        ),
        vertical_slider=Slider(
            controller=controllers.LayerController(),
            values=CurrentLayerStack(PickStrategy.ANIMATED),
        )
    ),
    templates.MouseTracker(
        name="Scroll brush size or opacity",
        horizontal_slider=Slider(
            controller=controllers.BrushSizeController(),
            values=[
                1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 12, 14, 16, 20, 25, 30, 35, 40, 50, 60, 70, 80,
                100, 120, 160, 200, 250, 300, 350, 400, 450,
                500, 600, 700, 800, 900, 1000
            ]
        ),
        vertical_slider=Slider(
            controller=controllers.OpacityController(),
            values=Range(10, 100),
            pixels_in_unit=5,
        ),
    ),
]
