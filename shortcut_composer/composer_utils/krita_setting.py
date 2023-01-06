from typing import Any
from api_krita import Krita


def read_setting(name: str, default: str) -> str:
    return Krita.read_setting(
        group="ShortcutComposer",
        name=name,
        default=default,
    )


def write_setting(name: str, value: Any):
    return Krita.write_setting(
        group="ShortcutComposer",
        name=name,
        value=value,
    )
