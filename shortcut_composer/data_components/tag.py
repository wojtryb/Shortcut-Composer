from typing import List
from api_krita.wrappers import Database


class Tag(List[str]):
    def __init__(self, tag_name: str):
        self.tag_name = tag_name
        self.extend(self._read_brushes())

    def _read_brushes(self):
        with Database() as database:
            return database.get_preset_names_from_tag(self.tag_name)
