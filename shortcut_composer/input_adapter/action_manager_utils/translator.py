# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

class Translator:
    """Substitutes non-latin signs with their QWERTY equivalents."""

    DEFAULT = "`QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./"
    """Template of signs in latin QWERTY layout."""

    LAYOUTS = {
        "cyryllic": "ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.",
        "arabic":   "ذضصثقفغعهخحجدشسيبلاتنمكطئءؤرﻻىةوزظ",
    }
    """Signs in non-latin alphabets in the same order as in QWERTY."""

    def __init__(self) -> None:
        signs_to_translate = ""
        for layout in self.LAYOUTS.values():
            signs_to_translate += layout

        self.table = str.maketrans(
            signs_to_translate,
            self.DEFAULT*len(self.LAYOUTS))

    def translate(self, x: str):
        """Substitute non-latin signs with their QWERTY equivalents."""
        return x.translate(self.table)
