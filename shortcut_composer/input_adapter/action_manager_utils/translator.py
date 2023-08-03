# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple


class Translation(NamedTuple):
    language: str
    """Signs in non-latin alphabets in the same order as in QWERTY."""
    template: str
    """Template of signs in latin QWERTY layout."""


class Translator:
    """Substitutes non-latin signs with their QWERTY equivalents."""

    TRANSLATIONS = {
        "cyryllic": Translation(
            language="ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ",
            template="`QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,."),
        "german": Translation(
            language="ÜÖÄ",
            template="[;'"),
        "greek": Translation(
            language="ΣΕΡΤΥΘΙΟΠΑΔΦΓΗΞΚΛΖΧΨΩΒΝΜ",
            template="WERTYUIOPADFGHJKLZXCVBNM"),
        "georgian": Translation(
            language="„ქწერტყუიოპასდფგჰჯკლზხცვბნმ",
            template="`QWERTYUIOPASDFGHJKLZXCVBNM"),
        "arabic": Translation(
            language="ذضصثقفغعهخحجدشسيبلاتنمكطئءؤرﻻىةوزظ",
            template="`QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./"),
    }

    def __init__(self) -> None:
        full_language = ""
        full_template = ""
        for language, template in self.TRANSLATIONS.values():
            if len(language) != len(template):
                raise RuntimeError(
                    f"Length of language does not match: {language, template}")
            full_language += language
            full_template += template

        self.table = str.maketrans(full_language, full_template)

    def translate(self, x: str):
        """Substitute non-latin signs with their QWERTY equivalents."""
        return x.translate(self.table)
