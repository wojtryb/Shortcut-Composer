from typing import List, Protocol
from enum import Enum

from templates.pie_menu_utils import Label


class GroupManager(Protocol):
    def fetch_groups(self) -> list: ...
    def get_values(self, group: str) -> list: ...
    def create_labels(self, values: List[Enum]) -> List[Label]: ...
