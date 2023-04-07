# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita


def fix_config():
    """Rewrites config values from their position in 1.1.1 to 1.2.0."""
    def fix(group: str, old_name: str, new_name: str):
        if Krita.read_setting(group, new_name, "not given") != "not given":
            return
        value = Krita.read_setting("ShortcutComposer", old_name, "not given")
        if value != "not given":
            Krita.write_setting(group, new_name, value)

    data = (
        ("Pick brush presets (red)", "Tag (red)", "Tag"),
        ("Pick brush presets (green)", "Tag (green)", "Tag"),
        ("Pick brush presets (blue)", "Tag (blue)", "Tag"),

        ("Pick brush presets (red)", "Tag (red) values", "Values"),
        ("Pick brush presets (green)", "Tag (green) values", "Values"),
        ("Pick brush presets (blue)", "Tag (blue) values", "Values"),

        ("Pick painting blending modes", "Blending modes values", "Values"),
        ("Pick misc tools", "Misc tools values", "Values"),
        ("Cycle selection tools", "Selection tools values", "Values"),
        ("Pick transform tool modes", "Transform modes values", "Values"),
        (
            "Create painting layer with blending mode",
            "Create blending layer values",
            "Values"),
    )

    for group, old_name, new_name in data:
        fix(f"ShortcutComposer: {group}", old_name, new_name)
