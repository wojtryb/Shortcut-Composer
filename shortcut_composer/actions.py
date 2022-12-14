"""
Implementation of all plugin actions.

Remember to define every action under exactly the same name in the
`shortcut_composer.action` file. Otherwise the action will not be
visible in `keyboard shortcuts` menu in krita settings.
"""

from PyQt5.QtGui import QColor
import templates
from api_krita.enums import BlendingMode, Tool, Toggle
from core_components import instructions, controllers
from data_components import (
    CurrentLayerStack,
    PickStrategy,
    read_setting,
    Slider,
    Range,
    Tag,
)


def create_actions(): return [

    # Switch between FREEHAND BRUSH and the MOVE tool
    templates.TemporaryKey(
        name="Temporary move tool",
        controller=controllers.ToolController(),
        low_value=Tool.FREEHAND_BRUSH,
        high_value=Tool.MOVE,
    ),

    # Switch between FREEHAND BRUSH and the TRANSFORM tool
    templates.TemporaryKey(
        name="Temporary transform tool",
        controller=controllers.ToolController(),
        low_value=Tool.FREEHAND_BRUSH,
        high_value=Tool.TRANSFORM,
        short_vs_long_press_time=1.0
    ),

    # Switch the eraser toggle ON and OFF
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    # Ensure the preserve alpha is OFF
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

    # Switch the preserve alpha toggle ON and OFF
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    # Ensure the eraser toggle is OFF
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
        values=[70, 50, 30, 100],
    ),

    # Cycle between selection tools from values_to_cycle list.
    # After a long key press, go back to the FREEHAND BRUSH tool
    templates.MultipleAssignment(
        name="Cycle selection tools",
        controller=controllers.ToolController(),
        default_value=Tool.FREEHAND_BRUSH,
        values=[
            Tool.FREEHAND_SELECTION,
            Tool.RECTANGULAR_SELECTION,
            Tool.CONTIGUOUS_SELECTION,
        ],
    ),


    # Control undo and redo actions by sliding the cursor horizontally
    # Start triggering the actions after passing a deadzone of 100 px
    # Use UndoOnPress instruction to trigger undo key press
    templates.MouseTracker(
        name="Scroll undo stack",
        instructions=[instructions.UndoOnPress()],
        horizontal_slider=Slider(
            controller=controllers.UndoController(),
            values=Range(float('-inf'), float('inf')),
            deadzone=100,
        ),
    ),

    # Scroll all active layers by sliding the cursor vertically
    # Use TemporaryOn instruction to temporarily isolate active layer
    templates.MouseTracker(
        name="Scroll isolated layers",
        instructions=[instructions.TemporaryOn(Toggle.ISOLATE_LAYER)],
        vertical_slider=Slider(
            controller=controllers.ActiveLayerController(),
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
            controller=controllers.ActiveLayerController(),
            values=CurrentLayerStack(PickStrategy.PINNED),
        ),
    ),

    # Scroll brush sizes by sliding the cursor horizontally or
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

    templates.PieMenu(
        name="Pick painting blending modes",
        controller=controllers.BlendingModeController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        values=[
            BlendingMode.NORMAL,
            BlendingMode.OVERLAY,
            BlendingMode.COLOR,
            BlendingMode.MULTIPLY,
            BlendingMode.ADD,
            BlendingMode.SCREEN,
            BlendingMode.BEHIND,
            BlendingMode.DARKEN,
            BlendingMode.LIGHTEN,
        ],
    ),

    templates.PieMenu(
        name="Pick misc tools",
        controller=controllers.ToolController(),
        values=[
            Tool.CROP,
            Tool.REFERENCE,
            Tool.GRADIENT,
            Tool.MULTI_BRUSH,
            Tool.ASSISTANTS,
        ],
    ),

    # Pick a brush preset from the tag named "RGBA" using a pie menu
    templates.PieMenu(
        name="Pick brush presets (red)",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        values=Tag(read_setting(name="Tag (red)", default="Erasers")),
        area_color=QColor(95, 65, 65, 190),
        active_color=QColor(200, 70, 70),
    ),

    templates.PieMenu(
        name="Pick brush presets (green)",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        values=Tag(read_setting(name="Tag (green)", default="RGBA")),
        area_color=QColor(65, 95, 65, 190),
        active_color=QColor(70, 200, 70),
    ),

    templates.PieMenu(
        name="Pick brush presets (blue)",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        values=Tag(read_setting(name="Tag (blue)", default="Pixel Art")),
        area_color=QColor(65, 65, 96, 190),
        active_color=QColor(100, 100, 230),
    ),
]
