from dataclasses import dataclass
from .krita_api_wrapper import KritaDatabase


class Tag:
    def __init__(self, tag: str) -> None:
        self.name = tag
        with KritaDatabase() as database:
            preset_names = database.get_preset_names_from_tag(tag)
        self.data = sorted(set(preset_names))

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: int):
        return self.data[index]


@dataclass
class Range:
    min: float
    max: float
