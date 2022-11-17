from api_krita.wrappers import Database


class Tag:
    """
    List-like container representating presets in a tag.

    Created using tag's name, gets filled with preset names.
    Does not update in runtime as the tag gets edited.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        with Database() as database:
            preset_names = database.get_preset_names_from_tag(name)
        self.data = sorted(set(preset_names))

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: int):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def index(self, value: str):
        return self.data.index(value)
