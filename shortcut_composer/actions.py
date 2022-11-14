"""File that acts as config - define all action objects here."""

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
        action_name="Move tool (temporary)",
        controller=controllers.ToolController(),
        high_value=Tool.MOVE,
    ),
    templates.TemporaryKey(
        action_name="Transform tool (temporary)",
        controller=controllers.ToolController(),
        high_value=Tool.TRANSFORM,
        time_interval=1.0
    ),
    templates.TemporaryKey(
        action_name="Eraser (temporary)",
        controller=controllers.ToggleController(Toggle.ERASER),
        low_value=False,
        high_value=True,
        instructions=[
            instructions.SetBrushOnNonPaintable(),
            instructions.EnsureOff(Toggle.PRESERVE_ALPHA),
        ],
    ),
    templates.TemporaryKey(
        action_name="Preserve alpha (temporary)",
        controller=controllers.ToggleController(Toggle.PRESERVE_ALPHA),
        low_value=False,
        high_value=True,
        instructions=[
            instructions.SetBrushOnNonPaintable(),
            instructions.EnsureOff(Toggle.ERASER),
        ],
    ),
    templates.RawInstructions(
        action_name="Toggle visibility (temporary)",
        instructions=[instructions.ToggleLayerVisibility()],
    ),
    templates.RawInstructions(
        action_name="Toggle show below (temporary)",
        instructions=[instructions.ToggleShowBelow()],
    ),
    templates.MultipleAssignment(
        action_name="Opacity (cycle)",
        controller=controllers.OpacityController(),
        default_value=100,
        values_to_cycle=[70, 50, 30, 100],
    ),
    templates.MultipleAssignment(
        action_name="Selection tools (cycle)",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.FREEHAND_SELECTION,
            Tool.RECTANGULAR_SELECTION,
            Tool.CONTIGUOUS_SELECTION,
        ],
    ),
    templates.MultipleAssignment(
        action_name="Misc tools (cycle)",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.CROP,
            Tool.REFERENCE,
            Tool.GRADIENT,
            Tool.MULTI_BRUSH,
        ],
    ),
    templates.MultipleAssignment(
        action_name="Preset (cycle)",
        controller=controllers.PresetController(),
        default_value="b) Basic-5 Size Opacity",
        values_to_cycle=Tag("Digital"),
        instructions=[instructions.SetBrushOnNonPaintable()],
    ),
    templates.MouseTracker(
        action_name="Layer scraper (tracker)",
        instructions=[instructions.TemporaryOn(Toggle.ISOLATE_LAYER)],
        vertical_slider=Slider(
            controller=controllers.LayerController(),
            values=CurrentLayerStack(PickStrategy.ALL),
        )
    ),
    templates.MouseTracker(
        action_name="Timeline scraper (tracker)",
        horizontal_slider=Slider(
            controller=controllers.TimeController(),
            values=Range(0, float('inf')),
        )
    ),
    templates.MouseTracker(
        action_name="Blending mode (tracker)",
        horizontal_slider=Slider(
            controller=controllers.BlendingModeController(),
            values=[
                BlendingMode.NORMAL,
                BlendingMode.OVERLAY,
                BlendingMode.MULTIPLY,
                BlendingMode.COLOR,
                BlendingMode.ADD,
                BlendingMode.BEHIND,
                BlendingMode.DARKEN,
                BlendingMode.LIGHTEN,
            ],
        ),
    ),
    templates.MouseTracker(
        action_name="Brush basic settings (tracker)",
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
            values=Range(10, 100)
        ),
    ),
]
