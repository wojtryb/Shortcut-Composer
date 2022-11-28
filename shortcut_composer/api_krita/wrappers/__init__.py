"""
Wrappers of classes in krita API.

Adds typing, dosctrings and changes the interface to be PEP8 compatibile.
"""

from .tool_descriptor import ToolDescriptor
from .database import Database
from .document import Document
from .canvas import Canvas
from .cursor import Cursor
from .node import Node
from .view import View

__all__ = [
    "ToolDescriptor",
    "Database",
    "Document",
    "Canvas",
    "Cursor",
    "Node",
    "View",
]
