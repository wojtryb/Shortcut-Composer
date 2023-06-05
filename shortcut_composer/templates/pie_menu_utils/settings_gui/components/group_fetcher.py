from typing import List, Type, Protocol

from api_krita.wrappers import Database
from api_krita.enums.helpers import EnumGroup


class GroupFetcher(Protocol):
    def fetch_groups(self) -> List[str]: ...


class EnumGroupFetcher:
    def __init__(self, enum_type: Type[EnumGroup]) -> None:
        self._enum_type = enum_type

    def fetch_groups(self) -> List[str]:
        return list(self._enum_type._groups_.keys())


class PresetGroupFetcher:
    def fetch_groups(self) -> List[str]:
        with Database() as database:
            return database.get_brush_tags()
