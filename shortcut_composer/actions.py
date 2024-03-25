# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Implementation of complex actions.

NOTE: Make sure that every complex action implemented here has a
definition in `shortcut_composer.action` file. Otherwise the action
will not be visible in `keyboard shortcuts` menu in krita settings.
"""

import templates

from PyQt5.QtGui import QColor

from api_krita.enums import Action, Tool, Toggle, BlendingMode, TransformMode
from core_components import instructions, controllers
from data_components import (
    RotationDeadzoneStrategy,
    PieDeadzoneStrategy,
    CurrentLayerStack,
    PickStrategy,
    Slider,
    Range,
    Tag)

INFINITY = float("inf")


def create_actions() -> list[templates.RawInstructions]: return [
    # Switch between FREEHAND BRUSH and the MOVE tool
    templates.TemporaryKey(
        name="Temporary move tool",
        controller=controllers.ToolController(),
        low_value=Tool.FREEHAND_BRUSH,
        high_value=Tool.MOVE,
    ),

    # Switch the eraser toggle ON and OFF
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    # Ensure the preserve alpha is OFF
    templates.TemporaryKey(
        name="Temporary eraser",
        controller=controllers.ToggleController(Toggle.ERASER),
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
        instructions=[instructions.SetBrushOnNonPaintable()],
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
    templates.CursorTracker(
        name="Scroll undo stack",
        instructions=[instructions.UndoOnPress()],
        horizontal_slider=Slider(
            controller=controllers.UndoController(),
            values=Range(-INFINITY, INFINITY),
            deadzone=100,
        ),
    ),

    # Scroll all active layers by sliding the cursor vertically
    # Use TemporaryOn instruction to temporarily isolate active layer
    templates.CursorTracker(
        name="Scroll isolated layers",
        instructions=[instructions.TemporaryOn(Toggle.ISOLATE_LAYER)],
        vertical_slider=Slider(
            controller=controllers.ActiveLayerController(),
            values=CurrentLayerStack(PickStrategy.ALL),
        ),
    ),

    # Scroll timeline by sliding the cursor horizontally or
    # animated layers by sliding it vertically
    #
    # Use TemporaryOn instruction to temporarily isolate active layer
    templates.CursorTracker(
        name="Scroll timeline or animated layers",
        instructions=[instructions.TemporaryOn(Toggle.ISOLATE_LAYER)],
        horizontal_slider=Slider(
            controller=controllers.TimeController(),
            values=Range(0, INFINITY),
        ),
        vertical_slider=Slider(
            controller=controllers.ActiveLayerController(),
            values=CurrentLayerStack(PickStrategy.PINNED),
        ),
    ),

    # Scroll brush sizes by sliding the cursor horizontally or
    # brush opacity layers by sliding it vertically
    #
    # Opacity is contiguous from 10% to 100%, sizes come from a list
    # Switch 1% of opacity every 5 px (instead of default 50 px)
    templates.CursorTracker(
        name="Scroll brush size or opacity",
        horizontal_slider=Slider(
            controller=controllers.BrushSizeController(),
            values=[
                1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 12, 14, 16, 20, 25, 30, 35, 40, 50, 60, 70, 80,
                100, 120, 160, 200, 250, 300, 350, 400, 450,
                500, 600, 700, 800, 900, 1000
            ],
            sensitivity_scale=2,
        ),
        vertical_slider=Slider(
            controller=controllers.OpacityController(),
            values=Range(10, 100),
            sensitivity_scale=10,
        ),
    ),

    # Scroll canvas rotation sizes by sliding the cursor
    # horizontally or canvas zoom by sliding it vertically
    templates.CursorTracker(
        name="Scroll canvas zoom or rotation",
        horizontal_slider=Slider(
            controller=controllers.CanvasRotationController(),
            values=Range(-INFINITY, INFINITY),
            sensitivity_scale=10,
        ),
        vertical_slider=Slider(
            controller=controllers.CanvasZoomController(),
            values=Range(0, INFINITY),
            sensitivity_scale=10,
        ),
    ),

    # Use pie menu to pick one of the tools.
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
        pie_radius_scale=0.9,
    ),


    # Use pie menu to pick one of the actions
    templates.PieMenu(
        name="Activate krita action (red)",
        controller=controllers.ActionController(),
        values=[
            Action.HORIZONTAL_MIRROR_TOOL,
            Action.WRAP_AROUND_MODE,
            Action.ERASER,
            Action.PRESERVE_ALPHA,
            Action.MIRROR_CANVAS,
        ],
        background_color=QColor(95, 65, 65, 190),
        active_color=QColor(200, 70, 70),
    ),

    # Use pie menu to pick one of the actions
    templates.PieMenu(
        name="Activate krita action (green)",
        controller=controllers.ActionController(),
        values=[
            Action.CREATE_BLANK_FRAME,
            Action.CREATE_DUPLICATE_FRAME,
            Action.REMOVE_KEYFRAME,
            Action.VIEW_ONION_SKIN,
            Action.RECORD_TIMELAPSE,
        ],
        background_color=QColor(65, 95, 65, 190),
        active_color=QColor(70, 200, 70),
    ),

    # Use pie menu to pick one of the actions
    templates.PieMenu(
        name="Activate krita action (blue)",
        controller=controllers.ActionController(),
        values=[
            Action.ADD_PAINT_LAYER,
            Action.TOGGLE_LAYER_VISIBILITY,
            Action.TOGGLE_LAYER_ALPHA_INHERITANCE,
            Action.TOGGLE_LAYER_ALPHA,
            Action.TOGGLE_LAYER_LOCK,
        ],
        background_color=QColor(70, 70, 105, 190),
        active_color=QColor(110, 160, 235),
    ),

    # Use pie menu to pick one of the brush blending modes.
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    templates.PieMenu(
        name="Pick painting blending modes",
        controller=controllers.BlendingModeController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        deadzone_strategy=PieDeadzoneStrategy.PICK_TOP,
        values=[
            BlendingMode.NORMAL,
            BlendingMode.OVERLAY,
            BlendingMode.COLOR,
            BlendingMode.MULTIPLY,
            BlendingMode.ADD,
            BlendingMode.SCREEN,
            BlendingMode.DARKEN,
            BlendingMode.LIGHTEN,
        ],
    ),

    # Use pie menu to create painting layer with selected blending mode.
    templates.PieMenu(
        name="Create painting layer with blending mode",
        controller=controllers.CreateLayerWithBlendingController(),
        values=[
            BlendingMode.NORMAL,
            BlendingMode.ERASE,
            BlendingMode.OVERLAY,
            BlendingMode.COLOR,
            BlendingMode.MULTIPLY,
            BlendingMode.ADD,
            BlendingMode.SCREEN,
            BlendingMode.DARKEN,
            BlendingMode.LIGHTEN,
        ],
    ),

    # Pick one of the transform tool modes.
    templates.PieMenu(
        name="Pick transform tool modes",
        controller=controllers.TransformModeController(),
        deadzone_strategy=PieDeadzoneStrategy.PICK_TOP,
        values=[
            TransformMode.FREE,
            TransformMode.PERSPECTIVE,
            TransformMode.WARP,
            TransformMode.CAGE,
            TransformMode.LIQUIFY,
            TransformMode.MESH,
        ]
    ),

    # Use pie menu to pick one of stored presets.
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    templates.PieMenu(
        name="Pick brush presets (red)",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        deadzone_strategy=PieDeadzoneStrategy.PICK_PREVIOUS,
        values=Tag("★ My Favorites"),
        background_color=QColor(95, 65, 65, 190),
        active_color=QColor(200, 70, 70),
    ),

    # Use pie menu to pick one of stored presets.
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    templates.PieMenu(
        name="Pick brush presets (green)",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        deadzone_strategy=PieDeadzoneStrategy.PICK_PREVIOUS,
        values=Tag("RGBA"),
        background_color=QColor(65, 95, 65, 190),
        active_color=QColor(70, 200, 70),
    ),

    # Use pie menu to pick one of stored presets.
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    templates.PieMenu(
        name="Pick brush presets (blue)",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        deadzone_strategy=PieDeadzoneStrategy.PICK_PREVIOUS,
        values=Tag("Erasers"),
        background_color=QColor(70, 70, 105, 190),
        active_color=QColor(110, 160, 235),
    ),

    # Use pie menu to pick one of stored presets.
    # By default, preset names are stored in .kra document.
    # Set tool to FREEHAND BRUSH if current tool does not allow to paint
    templates.PieMenu(
        name="Pick local brush presets",
        controller=controllers.PresetController(),
        instructions=[instructions.SetBrushOnNonPaintable()],
        deadzone_strategy=PieDeadzoneStrategy.PICK_PREVIOUS,
        values=[],
        save_local=True,
        active_color=QColor(234, 172, 0),
    ),

    # Use rotation widget to rotate the canvas.
    templates.RotationSelector(
        name="Rotate canvas",
        controller=controllers.CanvasRotationController(),
        is_widget_hidden=False,
        is_counterclockwise=False,
        offset=0,
        inverse_zones=False,
        divisions=24,
        deadzone_strategy=RotationDeadzoneStrategy.KEEP_CHANGE,
    ),

    # Use rotation widget to rotate current brush preset.
    templates.RotationSelector(
        name="Rotate brush",
        controller=controllers.BrushRotationController(),
        is_widget_hidden=False,
        is_counterclockwise=True,
        offset=90,
        inverse_zones=False,
        divisions=24,
        deadzone_strategy=RotationDeadzoneStrategy.KEEP_CHANGE,
    ),

    # .......................................
    # Insert your actions implementation here
    # .......................................

]
