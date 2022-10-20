from krita import *
from .currentTool import getCurrentTool

from ..SETUP import CONNECTEDTOGGLES


# ------- tools functions -------'

def setTool(toolName):
    'activates a tool of passed name'
    Application.instance().action(toolName).trigger()


def setBrushTool():
    'activates a freehand brush tool'
    setTool("KritaShape/KisToolBrush")


def isToolSelected(toolName):
    'returns True if the passed tool is active'
    return getCurrentTool() == toolName

# '------- eraser functions -------'


def toggleEraser(arg=None):
    'changes the state of the eraser, may affect alpha lock'
    if CONNECTEDTOGGLES:
        Application.action("preserve_alpha").setChecked(False)
    Application.action("erase_action").trigger()


def isEraserActive(arg=None):
    'returns True if the eraser is active'
    kritaEraserAction = Application.action("erase_action")
    return kritaEraserAction.isChecked()

# '------- alpha functions -------'


def toggleAlphaLock(arg=None):
    'changes the state of the alpha lock, may affect the eraser'
    if CONNECTEDTOGGLES:
        Application.action("erase_action").setChecked(False)
    Application.action("preserve_alpha").trigger()


def isAlphaLocked(arg=None):
    'returns True if the alpha is locked'
    kritaEraserAction = Application.action("preserve_alpha")
    return kritaEraserAction.isChecked()
