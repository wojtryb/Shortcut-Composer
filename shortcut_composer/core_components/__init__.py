"""
Contains core components that can be used in configuration of templates.

Core components are obligatory elements for every action.

Abstract base classes are directly available from the module, while
concrete implementations are stored in respective packages.
"""

from .instruction_base import Instruction, InstructionHolder
from .controller_base import Controller

__all__ = [
    'InstructionHolder',
    'Instruction',
    'Controller',
]
