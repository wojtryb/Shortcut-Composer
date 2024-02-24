# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Components used by the implementations of Field."""

from .parsers import dispatch_parser, Parser

__all__ = ["dispatch_parser", "Parser"]
