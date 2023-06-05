from typing import Type, TypeVar
from core_components import Controller
from ..pie_config import PieConfig
from .preset_pie_config import PresetPieConfig
from .non_preset_pie_config import NonPresetPieConfig

T = TypeVar('T')


def dispatch_pie_config(controller: Controller[T]) -> Type[PieConfig[T]]:
    if issubclass(controller.TYPE, str):
        return PresetPieConfig   # type: ignore
    return NonPresetPieConfig
