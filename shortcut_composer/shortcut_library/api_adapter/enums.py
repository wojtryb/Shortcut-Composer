from enum import Enum


class Tool(Enum):
    FREEHAND_BRUSH = "KritaShape/KisToolBrush"
    FREEHAND_SELECTION = "KisToolSelectOutline"
    GRADIENT = "KritaFill/KisToolGradient"
    LINE = "KritaShape/KisToolLine"
    TRANSFORM = "KisToolTransform"
    MOVE = "KritaTransform/KisToolMove"
    RECTANGULAR_SELECTION = "KisToolSelectRectangular"
    CONTIGUOUS_SELECTION = "KisToolSelectContiguous"
    REFERENCE = "ToolReferenceImages"
    CROP = "KisToolCrop"
    BEZIER_PATH = "KisToolPath"
    FREEHAND_PATH = "KisToolPencil"
    POLYLINE = "KisToolPolyline"
    SHAPE_SELECT = "InteractionTool"
    ASSISTANTS = "KisAssistantTool"
    COLOR_SAMPLER = "KritaSelected/KisToolColorSampler"
    POLYGON = "KisToolPolygon"
    MEASUREMENT = "KritaShape/KisToolMeasure"
    TEXT = "SvgTextTool"
    ELLIPSE = "KritaShape/KisToolEllipse"
    FILL = "KritaFill/KisToolFill"
    BEZIER_SELECTION = "KisToolSelectPath"
    DYNAMIC_BRUSH = "KritaShape/KisToolDyna"
    RECTANGLE = "KritaShape/KisToolRectangle"
    PAN = "PanTool"
    MULTI_BRUSH = "KritaShape/KisToolMultiBrush"
    EDIT_SHAPES = "PathTool"
    ELIPTICAL_SELECTION = "KisToolSelectElliptical"
    SMART_PATCH = "KritaShape/KisToolSmartPatch"
    COLORIZE_MASK = "KritaShape/KisToolLazyBrush"
    SIMILAR_COLOR_SELECTION = "KisToolSelectSimilar"
    ZOOM = "ZoomTool"
    MAGNETIC_SELECTION = "KisToolSelectMagnetic"
    CALLIGRAPHY = "KarbonCalligraphyTool"
    POLYGONAL_SELECTION = "KisToolSelectPolygonal"

    __PAINTABLE = {
        FREEHAND_BRUSH,
        LINE,
        ELLIPSE,
        DYNAMIC_BRUSH,
        RECTANGLE,
        MULTI_BRUSH,
        POLYLINE,
    }

    @classmethod
    def is_paintable(cls, tool: 'Tool'):
        return tool in cls.__PAINTABLE.value


class BlendingMode(Enum):
    NORMAL = 'normal'
    ADD = 'add'
    BURN = 'burn'
    COLOR = 'color'
    DODGE = 'dodge'
    DARKEN = 'darken'
    DIVIDE = 'divide'
    ERASE = 'erase'
    LIGHTEN = 'lighten'
    LUMINIZE = 'luminize'
    MULTIPLY = 'multiply'
    OVERLAY = 'overlay'
    SATURATION = 'saturation'
    SCREEN = 'screen'
    SOFT_LIGHT_SVG = 'soft_light_svg'
    INVERSE_SUBTRACT = 'inverse_subtract'
    SUBTRACT = 'subtract'
    AND = 'and'
    CONVERSE = 'converse'
    IMPLICATION = 'implication'
    NAND = 'nand'
    NOR = 'nor'
    NOT_CONVERSE = 'not_converse'
    NOT_IMPLICATION = 'not_implication'
    OR = 'or'
    XNOR = 'xnor'
    XOR = 'xor'
    DARKER_COLOR = 'darker color'
    EASY_BURN = 'easy burn'
    FOG_DARKEN_IFS_ILLUSIONS = 'fog_darken_ifs_illusions'
    GAMMA_DARK = 'gamma_dark'
    SHADE_IFS_ILLUSIONS = 'shade_ifs_illusions'
    LINEAR_BURN = 'linear_burn'
    COLOR_HSI = 'color_hsi'
    DEC_INTENSITY = 'dec_intensity'
    DEC_SATURATION_HSI = 'dec_saturation_hsi'
    HUE_HSI = 'hue_hsi'
    INC_INTENSITY = 'inc_intensity'
    INC_SATURATION_HSI = 'inc_saturation_hsi'
    INTENSITY = 'intensity'
    SATURATION_HSI = 'saturation_hsi'
    DEC_LIGHTNESS = 'dec_lightness'
    COLOR_HSL = 'color_hsl'
    DEC_SATURATION_HSL = 'dec_saturation_hsl'
    HUE_HSL = 'hue_hsl'
    INC_LIGHTNESS = 'inc_lightness'
    INC_SATURATION_HSL = 'inc_saturation_hsl'
    LIGHTNESS = 'lightness'
    SATURATION_HSL = 'saturation_hsl'
    COLOR_HSV = 'color_hsv'
    DEC_SATURATION_HSV = 'dec_saturation_hsv'
    DEC_VALUE = 'dec_value'
    HUE_HSV = 'hue_hsv'
    INC_SATURATION_HSV = 'inc_saturation_hsv'
    INC_VALUE = 'inc_value'
    SATURATION_HSV = 'saturation_hsv'
    VALUE = 'value'
    DEC_SATURATION = 'dec_saturation'
    DEC_LUMINOSITY = 'dec_luminosity'
    HUE = 'hue'
    INC_LUMINOSITY = 'inc_luminosity'
    INC_SATURATION = 'inc_saturation'
    EASY_DODGE = 'easy dodge'
    FLAT_LIGHT = 'flat_light'
    GAMMA_ILLUMINATION = 'gamma_illumination'
    FOG_LIGHTEN_IFS_ILLUSIONS = 'fog_lighten_ifs_illusions'
    GAMMA_LIGHT = 'gamma_light'
    HARD_LIGHT = 'hard_light'
    LIGHTER_COLOR = 'lighter color'
    LINEAR_DODGE = 'linear_dodge'
    LINEAR_LIGHT = 'linear light'
    LUMINOSITY_SAI = 'luminosity_sai'
    PNORM_A = 'pnorm_a'
    PNORM_B = 'pnorm_b'
    PIN_LIGHT = 'pin_light'
    SOFT_LIGHT_IFS_ILLUSIONS = 'soft_light_ifs_illusions'
    SOFT_LIGHT_PEGTOP_DELPHI = 'soft_light_pegtop_delphi'
    SOFT_LIGHT = 'soft_light'
    SUPER_LIGHT = 'super_light'
    TINT_IFS_ILLUSIONS = 'tint_ifs_illusions'
    VIVID_LIGHT = 'vivid_light'
    BUMPMAP = 'bumpmap'
    COMBINE_NORMAL = 'combine_normal'
    COPY = 'copy'
    COPY_BLUE = 'copy_blue'
    COPY_GREEN = 'copy_green'
    COPY_RED = 'copy_red'
    DISSOLVE = 'dissolve'
    TANGENT_NORMALMAP = 'tangent_normalmap'
    ALLANON = 'allanon'
    ALPHADARKEN = 'alphadarken'
    BEHIND = 'behind'
    DESTINATION_ATOP = 'destination-atop'
    DESTINATION_IN = 'destination-in'
    GEOMETRIC_MEAN = 'geometric_mean'
    GRAIN_EXTRACT = 'grain_extract'
    GRAIN_MERGE = 'grain_merge'
    GREATER = 'greater'
    HARD_MIX = 'hard mix'
    HARD_MIX_PHOTOSHOP = 'hard_mix_photoshop'
    HARD_MIX_SOFTER_PHOTOSHOP = 'hard_mix_softer_photoshop'
    HARD_OVERLAY = 'hard overlay'
    INTERPOLATION = 'interpolation'
    INTERPOLATION_2X = 'interpolation 2x'
    PARALLEL = 'parallel'
    PENUMBRA_A = 'penumbra a'
    PENUMBRA_B = 'penumbra b'
    PENUMBRA_C = 'penumbra c'
    PENUMBRA_D = 'penumbra d'
    DIVISIVE_MODULO = 'divisive_modulo'
    DIVISIVE_MODULO_CONTINUOUS = 'divisive_modulo_continuous'
    MODULO_CONTINUOUS = 'modulo_continuous'
    MODULO_SHIFT = 'modulo_shift'
    MODULO_SHIFT_CONTINUOUS = 'modulo_shift_continuous'
    ADDITIVE_SUBTRACTIVE = 'additive_subtractive'
    ARC_TANGENT = 'arc_tangent'
    DIFF = 'diff'
    EQUIVALENCE = 'equivalence'
    EXCLUSION = 'exclusion'
    NEGATION = 'negation'
    FREEZE = 'freeze'
    FREEZE_REFLECT = 'freeze_reflect'
    GLOW = 'glow'
    GLOW_HEAT = 'glow_heat'
    HEAT = 'heat'
    HEAT_GLOW = 'heat_glow'
    HEAT_GLOW_FREEZE_REFLECT_HYBRID = 'heat_glow_freeze_reflect_hybrid'
    REFLECT = 'reflect'
    REFLECT_FREEZE = 'reflect_freeze'
