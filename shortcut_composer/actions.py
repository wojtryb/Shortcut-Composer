"""File that acts as config - define all action objects here."""

from .composer_library.api.enums import BlendingMode, Tool
from .composer_library.api.wrappers import Tag

from .composer_library import templates
from .composer_library.templates import PickStrategy
from .composer_library.templates.slider_utils import Slider, Range

from .composer_library.components import instructions, controllers
from .composer_library.components.controllers.strategies \
    import SetBrushStrategy


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
        controller=controllers.EraserController(
            affect_preserve_alpha=True,
            set_brush_strategy=SetBrushStrategy.ON_NON_PAINTABLE
        ),
        low_value=False,
        high_value=True,
    ),
    templates.TemporaryKey(
        action_name="Preserve alpha (temporary)",
        controller=controllers.PreserveAlphaController(
            affect_eraser=True,
            set_brush_strategy=SetBrushStrategy.ON_NON_PAINTABLE
        ),
        low_value=False,
        high_value=True,
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
        controller=controllers.PresetController(
            set_brush_strategy=SetBrushStrategy.ON_NON_PAINTABLE
        ),
        default_value="b) Basic-5 Size Opacity",
        values_to_cycle=Tag("Digital")
    ),
    templates.LayerPicker(
        action_name="Layer scraper - isolate",
        additional_instructions=[instructions.IsolateLayer()],
        pick_strategy=PickStrategy.ALL
    ),
    templates.LayerPicker(
        action_name="Layer scraper - visibility",
        additional_instructions=[instructions.ToggleLayerVisibility()],
        pick_strategy=PickStrategy.VISIBLE
    ),
    templates.MouseTracker(
        action_name="Blending mode (tracker)",
        horizontal_slider=Slider(
            controller=controllers.BrushSizeController(),
            default_value=BlendingMode.NORMAL,
            values_to_cycle=[
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
        action_name="Discrete brush settings (tracker)",
        horizontal_slider=Slider(
            controller=controllers.BrushSizeController(),
            default_value=100,
            values_to_cycle=[
                0.7, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9,
                10, 12, 14, 16, 20, 25, 30, 35, 40, 50, 60, 70, 80,
                100, 120, 160, 200, 250, 300, 350, 400, 450,
                500, 600, 700, 800, 900, 1000
            ]
        ),
        vertical_slider=Slider(
            controller=controllers.OpacityController(),
            default_value=100,
            values_to_cycle=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        ),
    ),
    templates.MouseTracker(
        action_name="Contiguous brush settings (tracker)",
        horizontal_slider=Slider(
            controller=controllers.BrushSizeController(),
            default_value=100,
            values_to_cycle=Range(50, 1000)
        ),
        vertical_slider=Slider(
            controller=controllers.OpacityController(),
            default_value=100,
            values_to_cycle=Range(10, 100)
        ),
    ),
]
