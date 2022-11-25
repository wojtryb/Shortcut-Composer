"""
The only python file directly run by krita during plugin initialization phase.

Runs the file with extension by importing everything from it.

Appending this file location to python PATH allows to directly import
main packages instead of using relative imports.
"""

import sys
import os

sys.path.append(directory := os.path.dirname(__file__))
from .shortcut_composer import *
sys.path.remove(directory)
