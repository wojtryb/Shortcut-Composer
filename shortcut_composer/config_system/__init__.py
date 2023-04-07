# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
System granting easier API to control krita configuration in .kritarc.

Consists of two classes: "Field" and "FieldGroup".
Read the documentation of those classes for more info.

Holds a subpackage with ui elements dependent on the introducad
configuration concept.
"""

from .field import Field
from .field_group import FieldGroup

__all__ = ["Field", "FieldGroup"]
