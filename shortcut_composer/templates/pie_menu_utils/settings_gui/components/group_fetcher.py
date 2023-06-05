from typing import List, Dict, Protocol, Union, Iterable, Optional
from enum import Enum

from api_krita.wrappers import Database
from core_components import Controller
from core_components.controllers import PresetController

from data_components import Tag
from api_krita import Krita

from ...label import Label


class GroupFetcher(Protocol):
    def fetch_groups(self) -> list: ...
    def get_values(self, group: str) -> list: ...
    def create_labels(self, values: List[Enum]) -> List[Label]: ...


class EnumGroupFetcher(GroupFetcher):
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        self._enum_type = self._controller.TYPE

    def fetch_groups(self) -> List[str]:
        return list(self._enum_type._groups_.keys())

    def get_values(self, group: str) -> List[Enum]:
        if group == "All":
            return list(self._enum_type._member_map_.values())
        return self._enum_type._groups_[group]

    def create_labels(self, values: List[Enum]) -> List[Label[Enum]]:
        """Create labels from list of preset names."""
        labels = [Label.from_value(v, self._controller) for v in values]
        return [label for label in labels if label is not None]


class PresetGroupFetcher(GroupFetcher):

    known_labels: Dict[str, Union[Label, None]] = {}

    def __init__(self) -> None:
        self._controller = PresetController()

    def fetch_groups(self) -> List[str]:
        with Database() as database:
            return database.get_brush_tags()

    def get_values(self, group: str) -> List[str]:
        if group == "All":
            return list(Krita.get_presets().keys())
        return Tag(group)

    def create_labels(self, values: Iterable[str]) -> List[Label[str]]:
        """Create labels from list of preset names."""
        labels: list[Optional[Label]] = []

        for preset in values:
            if preset in self.known_labels:
                label = self.known_labels[preset]
            else:
                label = Label.from_value(preset, self._controller)
                self.known_labels[preset] = label
            labels.append(label)

        return [label for label in labels if label is not None]
