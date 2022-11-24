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

    # Switch between freehand brush and the move tool
    templates.TemporaryKey(
        name="Temporary move tool",
        controller=controllers.ToolController(),
        low_value=Tool.FREEHAND_BRUSH,
        high_value=Tool.MOVE,
    ),

    # Switch between freehand brush and the transform tool
    templates.TemporaryKey(
        name="Temporary transform tool",
        controller=controllers.ToolController(),
        low_value=Tool.FREEHAND_BRUSH,
        high_value=Tool.TRANSFORM,
        time_interval=1.0
    ),

    # Switch the eraser toggle on and off
    # Set tool to freehand brush if current tool does not allow to paint
    # Ensure the preserve alpha is off
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

    # Switch the preserve alpha toggle on and off
    # Set tool to freehand brush if current tool does not allow to paint
    # Ensure the eraser toggle is off
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

    # Run the ToggleLayerVisibility instruction
    # It toggles the current layer's visibility on key press and release
    templates.RawInstructions(
        name="Preview current layer visibility",
        instructions=[instructions.ToggleLayerVisibility()],
    ),

    # Run the ToggleShowBelow instruction
    # It toggles the visibility of layers above
    templates.RawInstructions(
        name="Preview projection below",
        instructions=[instructions.ToggleVisibilityAbove()],
    ),

    # Cycle between painting opacity values from values_to_cycle list
    # After a long key press, go back to opacity of 100%
    templates.MultipleAssignment(
        name="Cycle painting opacity",
        controller=controllers.OpacityController(),
        default_value=100,
        values_to_cycle=[70, 50, 30, 100],
    ),

    # Cycle between selection tools from values_to_cycle list.
    # After a long key press, go back to the freehand brush tool
    templates.MultipleAssignment(
        name="Cycle selection tools",
        controller=controllers.ToolController(),
        default_value=Tool.FREEHAND_BRUSH,
        values_to_cycle=[
            Tool.FREEHAND_SELECTION,
            Tool.RECTANGULAR_SELECTION,
            Tool.CONTIGUOUS_SELECTION,
        ],
    ),

    # Cycle between miscellaneous tools from values_to_cycle list
    # After a long key press, go back to the freehand brush tool
    templates.MultipleAssignment(
        name="Cycle misc tools",
        controller=controllers.ToolController(),
        default_value=Tool.FREEHAND_BRUSH,
        values_to_cycle=[
            Tool.CROP,
            Tool.REFERENCE,
            Tool.GRADIENT,
            Tool.MULTI_BRUSH,
        ],
    ),

    # Cycle between painting blending modes from values_to_cycle list
    # After a long key press, go back to the normal blending mode
    templates.MultipleAssignment(
        name="Cycle painting blending modes",
        controller=controllers.BlendingModeController(),
        default_value=BlendingMode.NORMAL,
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

    # Cycle between brush presets from the tag named "Digital"
    # After a long key press, set "b) Basic-5 Size Opacity" preset
    templates.MultipleAssignment(
        name="Cycle brush presets",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        values_to_cycle=Tag("Digital"),
        default_value="b) Basic-5 Size Opacity",
    ),

    # Control undo and redo actions by sliding the cursor horizontally
    # Start triggering the actions after passing a deadzone of 100 px
    # Use UndoOnShortPress instruction to trigger undo on short press
    templates.MouseTracker(
        name="Scroll undo stack",
        instructions=[instructions.UndoOnShortPress()],
        horizontal_slider=Slider(
            controller=controllers.UndoController(),
            values=Range(float('-inf'), float('inf')),
            deadzone=100,
        ),
    ),

    # Scroll all active layer by sliding the cursor vertically
    # Use TemporaryOn instruction to temporarily isolate active layer
    templates.MouseTracker(
        name="Scroll isolated layers",
        instructions=[instructions.TemporaryOn(Toggle.ISOLATE_LAYER)],
        vertical_slider=Slider(
            controller=controllers.LayerController(),
            values=CurrentLayerStack(PickStrategy.ALL),
        ),
    ),

    # Scroll timeline by sliding the cursor horizontally or
    # animated layers by sliding it vertically

    # Use TemporaryOn instruction to temporarily isolate active layer
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
        ),
    ),

    # Scroll brush size by sliding the cursor horizontally or
    # brush opacity layers by sliding it vertically

    # Opacity is contiguous from 10% to 100%, sizes come from a list
    # Switch 1% of opacity every 5 px (instead of default 50 px)
    templates.MouseTracker(
        name="Scroll brush size or opacity",
        horizontal_slider=Slider(
            controller=controllers.BrushSizeController(),
            values=[
                1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 12, 14, 16, 20, 25, 30, 35, 40, 50, 60, 70, 80,
                100, 120, 160, 200, 250, 300, 350, 400, 450,
                500, 600, 700, 800, 900, 1000
            ],
        ),
        vertical_slider=Slider(
            controller=controllers.OpacityController(),
            values=Range(10, 100),
            pixels_in_unit=5,
        ),
    ),
]
