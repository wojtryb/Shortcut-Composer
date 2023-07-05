# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional
from .helpers import EnumGroup, Group


class BlendingMode(EnumGroup):
    """
    Contains all known blending modes in krita.

    Example usage: `BlendingMode.NORMAL`
    """

    _arithmetic = Group("Arithmetic")
    ADD = "add", "Addition"
    DIVIDE = "divide"
    INVERSE_SUBTRACT = "inverse_subtract"
    MULTIPLY = "multiply"
    SUBTRACT = "subtract"

    _binary = Group("Binary")
    AND = "and", "AND"
    CONVERSE = "converse", "CONVERSE"
    IMPLICATION = "implication", "IMPLICATION"
    NAND = "nand", "NAND"
    NOR = "nor", "NOR"
    NOT_CONVERSE = "not_converse", "NOT_CONVERSE"
    NOT_IMPLICATION = "not_implication", "NOT_IMPLICATION"
    OR = "or", "OR"
    XNOR = "xnor", "XNOR"
    XOR = "xor", "XOR"

    _darken = Group("Darken")
    BURN = "burn"
    DARKEN = "darken"
    DARKER_COLOR = "darker color"
    EASY_BURN = "easy burn"
    FOG_DARKEN_IFS_ILLUSIONS = (
        "fog_darken_ifs_illusions",
        "Fog Darken (IFS Illusions)")
    GAMMA_DARK = "gamma_dark"
    LINEAR_BURN = "linear_burn"
    SHADE_IFS_ILLUSIONS = (
        "shade_ifs_illusions"
        "Shade (IFS Illusions)")

    _hsi = Group("HSI")
    COLOR_HSI = "color_hsi", "Color HSI"
    DEC_INTENSITY = "dec_intensity", "Decrease Intensity"
    DEC_SATURATION_HSI = "dec_saturation_hsi", "Decrease Saturation HSI"
    HUE_HSI = "hue_hsi", "Hue HSI"
    INC_INTENSITY = "inc_intensity", "Increase Intensity"
    INC_SATURATION_HSI = "inc_saturation_hsi", "Increase Saturation HSI"
    INTENSITY = "intensity"
    SATURATION_HSI = "saturation_hsi", "Saturation HSI"

    _hsl = Group("HSL")
    COLOR_HSL = "color_hsl", "Color HSL"
    DEC_LIGHTNESS = "dec_lightness", "Decrease Lightness"
    DEC_SATURATION_HSL = "dec_saturation_hsl", "Decrease Saturation HSL"
    HUE_HSL = "hue_hsl", "Hue HSL"
    INC_LIGHTNESS = "inc_lightness", "Increase Lightness"
    INC_SATURATION_HSL = "inc_saturation_hsl", "Increase Saturation HSL"
    LIGHTNESS = "lightness"
    SATURATION_HSL = "saturation_hsl", "Saturation HSL"

    _hsv = Group("HSV")
    COLOR_HSV = "color_hsv", "Color HSV"
    DEC_SATURATION_HSV = "dec_saturation_hsv", "Decrease Saturation HSV"
    DEC_VALUE = "dec_value", "Decrease Value"
    HUE_HSV = "hue_hsv", "Hue HSV"
    INC_SATURATION_HSV = "inc_saturation_hsv", "Increase Saturation HSV"
    INC_VALUE = "inc_value", "Increase Value"
    SATURATION_HSV = "saturation_hsv", "Saturation HSV"
    VALUE = "value"

    _hsy = Group("HSY")
    COLOR = "color"
    DEC_LUMINOSITY = "dec_luminosity", "Decrease Luminosity"
    DEC_SATURATION = "dec_saturation", "Decrease Saturation"
    HUE = "hue"
    INC_LUMINOSITY = "inc_luminosity", "Increase Luminosity"
    INC_SATURATION = "inc_saturation", "Increase Saturation"
    LUMINIZE = "luminize"
    SATURATION = "saturation"

    _lighten = Group("Lighten")
    DODGE = "dodge"
    EASY_DODGE = "easy dodge"
    FLAT_LIGHT = "flat_light"
    FOG_LIGHTEN_IFS_ILLUSIONS = (
        "fog_lighten_ifs_illusions",
        "Fog Lighten (IFS Illusions)")
    GAMMA_ILLUMINATION = "gamma_illumination"
    GAMMA_LIGHT = "gamma_light"
    HARD_LIGHT = "hard_light"
    LIGHTEN = "lighten"
    LIGHTER_COLOR = "lighter color"
    LINEAR_DODGE = "linear_dodge"
    LINEAR_LIGHT = "linear light"
    LUMINOSITY_SAI = "luminosity_sai"
    PNORM_A = "pnorm_a", "P-Norm A"
    PNORM_B = "pnorm_b", "P-Norm B"
    PIN_LIGHT = "pin_light"
    SCREEN = "screen"
    SOFT_LIGHT_IFS_ILLUSIONS = (
        "soft_light_ifs_illusions",
        "Soft Light (IFS Illusions)")
    SOFT_LIGHT_PEGTOP_DELPHI = (
        "soft_light_pegtop_delphi"
        "Soft Light (Pegtio-Delphi)")
    SOFT_LIGHT = "soft_light", "Soft Light (Photoshop)"
    SOFT_LIGHT_SVG = "soft_light_svg", "Soft Light (SVG)"
    SUPER_LIGHT = "super_light"
    TINT_IFS_ILLUSIONS = "tint_ifs_illusions", "Tint (IFS Illusions)"
    VIVID_LIGHT = "vivid_light"

    _misc = Group("Misc")
    BUMPMAP = "bumpmap"
    COMBINE_NORMAL = "combine_normal", "Combine Normal Map"
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
    HARD_MIX_PHOTOSHOP = "hard_mix_photoshop", "Hard Mix (Photoshop)"
    HARD_MIX_SOFTER_PHOTOSHOP = (
        "hard_mix_softer_photoshop",
        "Hard Mix Softer (Photoshop)")
    HARD_OVERLAY = "hard overlay"
    INTERPOLATION = "interpolation"
    INTERPOLATION_2X = "interpolation 2x", "Interpolation - 2X"
    NORMAL = "normal"
    OVERLAY = "overlay"
    PARALLEL = "parallel"
    PENUMBRA_A = "penumbra a"
    PENUMBRA_B = "penumbra b"
    PENUMBRA_C = "penumbra c"
    PENUMBRA_D = "penumbra d"

    _modulo = Group("Modulo")
    DIVISIVE_MODULO = "divisive_modulo"
    DIVISIVE_MODULO_CONTINUOUS = (
        "divisive_modulo_continuous",
        "Divisive Modulo - Continuous")
    MODULO_CONTINUOUS = "modulo_continuous", "Modulo - Continuous"
    MODULO_SHIFT = "modulo_shift"
    MODULO_SHIFT_CONTINUOUS = (
        "modulo_shift_continuous",
        "Modulo Shift - Continuous")

    _negative = Group("Negative")
    ADDITIVE_SUBTRACTIVE = "additive_subtractive"
    ARC_TANGENT = "arc_tangent"
    DIFF = "diff"
    EQUIVALENCE = "equivalence"
    EXCLUSION = "exclusion"
    NEGATION = "negation"

    _quadratic = Group("Quadratic")
    FREEZE = "freeze"
    FREEZE_REFLECT = "freeze_reflect", "Freeze-Reflect"
    GLOW = "glow"
    GLOW_HEAT = "glow_heat", "Glow-Heat"
    HEAT = "heat"
    HEAT_GLOW = "heat_glow", "Heat-Glow"
    HEAT_GLOW_FREEZE_REFLECT_HYBRID = (
        "heat_glow_freeze_reflect_hybrid"
        "Heat-Glow & Freeze-Reflect Hybrid")
    REFLECT = "reflect"
    REFLECT_FREEZE = "reflect_freeze", "Reflect-Freeze"

    def __init__(self, value: str, pretty_name: Optional[str] = None):
        self._value_ = value
        self._custom_pretty_name = pretty_name

    @property
    def pretty_name(self) -> str:
        """Format blending mode name as in Krita Blending Mode combobox."""
        if self._custom_pretty_name is not None:
            return self._custom_pretty_name
        return self.name.replace("_", " ").title()
