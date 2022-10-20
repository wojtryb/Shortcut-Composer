from krita import *
from .currentTool import getCurrentTool

from ..SETUP import CONNECTEDTOGGLES


# ------- tools functions -------'

def setTool(toolName):
    'activates a tool of passed name'
    Application.instance().action(toolName).trigger()


def isToolSelected(toolName):
    'returns True if the passed tool is active'
    return getCurrentTool() == toolName

# '------- eraser functions -------'


def toggleEraser():
    'changes the state of the eraser, may affect alpha lock'
    if CONNECTEDTOGGLES:
        Application.action("preserve_alpha").setChecked(False)
    Application.action("erase_action").trigger()


def isEraserActive():
    'returns True if the eraser is active'
    kritaEraserAction = Application.action("erase_action")
    return kritaEraserAction.isChecked()

# '------- alpha functions -------'


def toggleAlphaLock():
    'changes the state of the alpha lock, may affect the eraser'
    if CONNECTEDTOGGLES:
        Application.action("erase_action").setChecked(False)
    Application.action("preserve_alpha").trigger()


def isAlphaLocked():
    'returns True if the alpha is locked'
    kritaEraserAction = Application.action("preserve_alpha")
    return kritaEraserAction.isChecked()
