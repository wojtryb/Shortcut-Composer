from krita import *
from .current_tool import get_current_tool_name

from ..SETUP import CONNECTEDTOGGLES


def set_tool(tool_name):
    'activates a tool of passed name'
    Application.instance().action(tool_name).trigger()


def is_tool_selected(tool_name):
    'returns True if the passed tool is active'
    return get_current_tool_name() == tool_name


def toggle_eraser():
    'changes the state of the eraser, may affect alpha lock'
    if CONNECTEDTOGGLES:
        Application.action("preserve_alpha").setChecked(False)
    Application.action("erase_action").trigger()


def is_eraser_active():
    'returns True if the eraser is active'
    kritaEraserAction = Application.action("erase_action")
    return kritaEraserAction.isChecked()


def toggle_alpha_lock():
    'changes the state of the alpha lock, may affect the eraser'
    if CONNECTEDTOGGLES:
        Application.action("erase_action").setChecked(False)
    Application.action("preserve_alpha").trigger()


def is_alpha_locked():
    'returns True if the alpha is locked'
    kritaEraserAction = Application.action("preserve_alpha")
    return kritaEraserAction.isChecked()
