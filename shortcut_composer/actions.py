"""File that acts as config - define all action objects here."""

from .composer_library.krita_api import controllers
from .composer_library.krita_api.enums import BlendingMode, Tool
from .composer_library.krita_api.wrappers import Tag
from .composer_library.krita_api.controllers.strategies import SetBrushStrategy
from .composer_library import shortcut_templates
from .composer_library.shortcut_templates.slider_utils import Slider, Range
from .composer_library.shortcut_templates import HideStrategy, PickStrategy


actions = [
    shortcut_templates.TemporaryKey(
        action_name="Eraser (toggle)",
        controller=controllers.EraserController(affect_preserve_alpha=True),
        low_value=False,
        high_value=True,
    ),
    shortcut_templates.TemporaryKey(
        action_name="Preserve alpha (toggle)",
        controller=controllers.PreserveAlphaController(affect_eraser=True),
        low_value=False,
        high_value=True,
    ),
    shortcut_templates.LayerPicker(
        action_name="Layer picker",
        hide_strategy=HideStrategy.MAKE_INVISIBLE,
        pick_strategy=PickStrategy.VISIBLE
    ),
    shortcut_templates.MouseTracker(
        action_name="Brush size mouse",
        separate_sliders=True,
        horizontal_slider=Slider(
            controller=controllers.BrushSizeController(),
            default_value=100,
            values_to_cycle=Range(1, 1000),
            sensitivity=0.5
        ),
        vertical_slider=Slider(
            controller=controllers.BrushSizeController(),
            default_value=100,
            values_to_cycle=[50, 100, 200, 250, 500, 1000]
        ),
    ),
    shortcut_templates.MouseTracker(
        action_name="Mouse cycle",
        separate_sliders=True,
        horizontal_slider=Slider(
            controller=controllers.OpacityController(),
            default_value=50,
            values_to_cycle=Range(10, 90)
        ),
        vertical_slider=Slider(
            controller=controllers.OpacityController(),
            default_value=50,
            values_to_cycle=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        ),
        # horizontal_slider=Slider(
        #     controllers=controllers.ToolController,
        #     default_value=Tool.FREEHAND_SELECTION,
        #     values_to_cycle=[
        #         Tool.FREEHAND_SELECTION,
        #         Tool.RECTANGULAR_SELECTION,
        #         Tool.CONTIGUOUS_SELECTION,
        #         Tool.GRADIENT,
        #         Tool.LINE,
        #         Tool.TRANSFORM,
        #         Tool.REFERENCE,
        #     ],
        # ),
        # vertical_slider=Slider(
        #     controllers=controllers.BlendingModeController(),
        #     values_to_cycle=[
        #         BlendingMode.OVERLAY,
        #         BlendingMode.NORMAL,
        #         BlendingMode.DARKEN],
        #     default_value=BlendingMode.NORMAL,
        #     sensitivity=50
        # ),
    ),
    shortcut_templates.MouseTracker(
        action_name="Canvas slider",
        separate_sliders=True,
        horizontal_slider=Slider(
            controller=controllers.CanvasRotationController(),
            default_value=0,
            values_to_cycle=Range(1, 90),
            sensitivity=50
        ),
        vertical_slider=Slider(
            controller=controllers.CanvasZoomController(),
            default_value=1,
            values_to_cycle=Range(0.25, 4),
            sensitivity=50
        ),
    ),
    shortcut_templates.TemporaryKey(
        action_name="Freehand selection (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.FREEHAND_SELECTION,
    ),
    shortcut_templates.TemporaryKey(
        action_name="Gradient (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.GRADIENT,
    ),
    shortcut_templates.TemporaryKey(
        action_name="Line tool (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.LINE,
    ),
    shortcut_templates.TemporaryKey(
        action_name="Transform tool (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.TRANSFORM,
        time_interval=1.0
    ),
    shortcut_templates.TemporaryKey(
        action_name="Move tool (toggle)",
        controller=controllers.ToolController(),
        high_value=Tool.MOVE,
    ),
    shortcut_templates.MultipleAssignment(
        action_name="Selections tools (cycle)",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.FREEHAND_SELECTION,
            Tool.RECTANGULAR_SELECTION,
            Tool.CONTIGUOUS_SELECTION,
        ],
    ),
    shortcut_templates.MultipleAssignment(
        action_name="Canvas cycle",
        controller=controllers.CanvasRotationController(),
        default_value=0,
        values_to_cycle=[15, 30, 60, 90],
    ),
    shortcut_templates.MultipleAssignment(
        action_name="Misc tools (cycle)",
        controller=controllers.ToolController(),
        values_to_cycle=[
            Tool.GRADIENT,
            Tool.LINE,
            Tool.TRANSFORM,
            Tool.REFERENCE,
        ],
    ),
    shortcut_templates.MultipleAssignment(
        action_name="Preset (cycle)",
        controller=controllers.PresetController(
            set_brush_strategy=SetBrushStrategy.ON_NON_PAINTABLE
        ),
        default_value="y) Texture Big",
        values_to_cycle=Tag("Digital")
    ),
    shortcut_templates.MultipleAssignment(
        action_name="Opacity (cycle)",
        controller=controllers.OpacityController(),
        values_to_cycle=[75, 50, 20.3, 11.1],
        include_default_in_cycle=True,
    ),
    shortcut_templates.MultipleAssignment(
        action_name="Blending mode (cycle)",
        controller=controllers.BlendingModeController(),
        values_to_cycle=[BlendingMode.OVERLAY],
        include_default_in_cycle=True,
    ),
]
