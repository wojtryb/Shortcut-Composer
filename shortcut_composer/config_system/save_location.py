from typing import Any, Optional
from enum import Enum
from .api_krita import Krita


class GlobalSettings:
    @staticmethod
    def write(group: str, name: str, value: Any):
        Krita.write_setting(group=group, name=name, value=value)

    @staticmethod
    def read(group: str, name: str, default: str = "Not stored")\
            -> Optional[str]:
        return Krita.read_setting(group=group, name=name, default=default)


class KritaDocumentSettings:
    @staticmethod
    def write(group: str, name: str, value: Any):
        document = Krita.get_active_document()
        if document is not None:
            document.write_annotation(f"{group} {name}", "",  str(value))

    @staticmethod
    def read(group: str, name: str, default: str = "Not stored")\
            -> Optional[str]:
        document = Krita.get_active_document()
        annotation_name = f"{group} {name}"

        if document is None \
                or not document.contains_annotation(annotation_name):
            return None if default == "Not stored" else default

        return document.read_annotation(annotation_name)


class SaveLocation(Enum):

    GLOBAL = GlobalSettings
    LOCAL = KritaDocumentSettings

    def write(self, group: str, name: str, value: Any) -> None:
        self.value.write(group, name, value)

    def read(self, group: str, name: str, default: str = "Not stored")\
            -> Optional[str]:
        return self.value.read(group, name, default)
