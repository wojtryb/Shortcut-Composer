# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Wrappers of classes in krita API.

Adds typing, docstrings and changes the interface to be PEP8 compatible.
"""

from .tool_descriptor import ToolDescriptor
from .database import Database
from .document import Document
from .version import Version
from .canvas import Canvas
from .cursor import Cursor
from .node import Node
from .view import View

__all__ = [
    "ToolDescriptor",
    "Database",
    "Document",
    "Version",
    "Canvas",
    "Cursor",
    "Node",
    "View"]
