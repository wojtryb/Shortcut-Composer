from api_krita.wrappers import Database


class Tag(list):
    def __init__(self, default_tag_name: str):
        self.tag_name = default_tag_name
        self.extend(self._read_brushes())

    def _read_brushes(self):
        with Database() as database:
            return database.get_preset_names_from_tag(self.tag_name)
