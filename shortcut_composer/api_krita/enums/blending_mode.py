# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from .helpers import EnumGroup, Group


class BlendingMode(EnumGroup):
    """
    Contains all known blending modes in krita.

    Example usage: `BlendingMode.NORMAL`
    """

    _arithmetic = Group("Arithmetic")
    ADD = "add"
    DIVIDE = "divide"
    INVERSE_SUBTRACT = "inverse_subtract"
    MULTIPLY = "multiply"
    SUBTRACT = "subtract"

    _binary = Group("Binary")
    AND = "and"
    CONVERSE = "converse"
    IMPLICATION = "implication"
    NAND = "nand"
    NOR = "nor"
    NOT_CONVERSE = "not_converse"
    NOT_IMPLICATION = "not_implication"
    OR = "or"
    XNOR = "xnor"
    XOR = "xor"

    _darken = Group("Darken")
    BURN = "burn"
    DARKEN = "darken"
    DARKER_COLOR = "darker color"
    EASY_BURN = "easy burn"
    FOG_DARKEN_IFS_ILLUSIONS = "fog_darken_ifs_illusions"
    GAMMA_DARK = "gamma_dark"
    LINEAR_BURN = "linear_burn"
    SHADE_IFS_ILLUSIONS = "shade_ifs_illusions"

    _hsi = Group("HSI")
    COLOR_HSI = "color_hsi"
    DEC_INTENSITY = "dec_intensity"
    DEC_SATURATION_HSI = "dec_saturation_hsi"
    HUE_HSI = "hue_hsi"
    INC_INTENSITY = "inc_intensity"
    INC_SATURATION_HSI = "inc_saturation_hsi"
    INTENSITY = "intensity"
    SATURATION_HSI = "saturation_hsi"

    _hsl = Group("HSL")
    COLOR_HSL = "color_hsl"
    DEC_LIGHTNESS = "dec_lightness"
    DEC_SATURATION_HSL = "dec_saturation_hsl"
    HUE_HSL = "hue_hsl"
    INC_LIGHTNESS = "inc_lightness"
    INC_SATURATION_HSL = "inc_saturation_hsl"
    LIGHTNESS = "lightness"
    SATURATION_HSL = "saturation_hsl"

    _hsv = Group("HSV")
    COLOR_HSV = "color_hsv"
    DEC_SATURATION_HSV = "dec_saturation_hsv"
    DEC_VALUE = "dec_value"
    HUE_HSV = "hue_hsv"
    INC_SATURATION_HSV = "inc_saturation_hsv"
    INC_VALUE = "inc_value"
    SATURATION_HSV = "saturation_hsv"
    VALUE = "value"

    _hsy = Group("HSY")
    COLOR = "color"
    DEC_LUMINOSITY = "dec_luminosity"
    DEC_SATURATION = "dec_saturation"
    HUE = "hue"
    INC_LUMINOSITY = "inc_luminosity"
    INC_SATURATION = "inc_saturation"
    LUMINIZE = "luminize"
    SATURATION = "saturation"

    _lighten = Group("Lighten")
    DODGE = "dodge"
    EASY_DODGE = "easy dodge"
    FLAT_LIGHT = "flat_light"
    FOG_LIGHTEN_IFS_ILLUSIONS = "fog_lighten_ifs_illusions"
    GAMMA_ILLUMINATION = "gamma_illumination"
    GAMMA_LIGHT = "gamma_light"
    HARD_LIGHT = "hard_light"
    LIGHTEN = "lighten"
    LIGHTER_COLOR = "lighter color"
    LINEAR_DODGE = "linear_dodge"
    LINEAR_LIGHT = "linear light"
    LUMINOSITY_SAI = "luminosity_sai"
    PNORM_A = "pnorm_a"
    PNORM_B = "pnorm_b"
    PIN_LIGHT = "pin_light"
    SOFT_LIGHT_IFS_ILLUSIONS = "soft_light_ifs_illusions"
    SOFT_LIGHT_PEGTOP_DELPHI = "soft_light_pegtop_delphi"
    SOFT_LIGHT = "soft_light"
    SOFT_LIGHT_SVG = "soft_light_svg"
    SCREEN = "screen"
    SUPER_LIGHT = "super_light"
    TINT_IFS_ILLUSIONS = "tint_ifs_illusions"
    VIVID_LIGHT = "vivid_light"

    _misc = Group("Misc")
    BUMPMAP = "bumpmap"
    COMBINE_NORMAL = "combine_normal"
    COPY = "copy"
    COPY_BLUE = "copy_blue"
    COPY_GREEN = "copy_green"
    COPY_RED = "copy_red"
    DISSOLVE = "dissolve"
    TANGENT_NORMALMAP = "tangent_normalmap"

    _mix = Group("Mix")
    ALLANON = "allanon"
    ALPHADARKEN = "alphadarken"
    BEHIND = "behind"
    DESTINATION_ATOP = "destination-atop"
    DESTINATION_IN = "destination-in"
    ERASE = "erase"
    GEOMETRIC_MEAN = "geometric_mean"
    GRAIN_EXTRACT = "grain_extract"
    GRAIN_MERGE = "grain_merge"
    GREATER = "greater"
    HARD_MIX = "hard mix"
    HARD_MIX_PHOTOSHOP = "hard_mix_photoshop"
    HARD_MIX_SOFTER_PHOTOSHOP = "hard_mix_softer_photoshop"
    HARD_OVERLAY = "hard overlay"
    INTERPOLATION = "interpolation"
    INTERPOLATION_2X = "interpolation 2x"
    NORMAL = "normal"
    OVERLAY = "overlay"
    PARALLEL = "parallel"
    PENUMBRA_A = "penumbra a"
    PENUMBRA_B = "penumbra b"
    PENUMBRA_C = "penumbra c"
    PENUMBRA_D = "penumbra d"

    _modulo = Group("Modulo")
    DIVISIVE_MODULO = "divisive_modulo"
    DIVISIVE_MODULO_CONTINUOUS = "divisive_modulo_continuous"
    MODULO_CONTINUOUS = "modulo_continuous"
    MODULO_SHIFT = "modulo_shift"
    MODULO_SHIFT_CONTINUOUS = "modulo_shift_continuous"

    _negative = Group("Negative")
    ADDITIVE_SUBTRACTIVE = "additive_subtractive"
    ARC_TANGENT = "arc_tangent"
    DIFF = "diff"
    EQUIVALENCE = "equivalence"
    EXCLUSION = "exclusion"
    NEGATION = "negation"

    _quadratic = Group("Quadratic")
    FREEZE = "freeze"
    FREEZE_REFLECT = "freeze_reflect"
    GLOW = "glow"
    GLOW_HEAT = "glow_heat"
    HEAT = "heat"
    HEAT_GLOW = "heat_glow"
    HEAT_GLOW_FREEZE_REFLECT_HYBRID = "heat_glow_freeze_reflect_hybrid"
    REFLECT = "reflect"
    REFLECT_FREEZE = "reflect_freeze"

    @property
    def pretty_name(self) -> str:
        """Format blending mode name like: `Darker color`."""
        return self.name.replace("_", " ").capitalize()
