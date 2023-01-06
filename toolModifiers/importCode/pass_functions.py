from krita import *
from .current_tool import get_current_tool_name

from ..config import connected_toggles


def set_tool(tool_name):
    'activates a tool of passed name'
    Application.action(tool_name).trigger()


def is_tool_selected(tool_name):
    'returns True if the passed tool is active'
    return get_current_tool_name() == tool_name


def toggle_eraser():
    'changes the state of the eraser, may affect alpha lock'
    if connected_toggles:
        Application.action("preserve_alpha").setChecked(False)
    Application.action("erase_action").trigger()


def is_eraser_active():
    'returns True if the eraser is active'
    krita_eraser_action = Application.action("erase_action")
    return krita_eraser_action.isChecked()


def toggle_alpha_lock():
    'changes the state of the alpha lock, may affect the eraser'
    if connected_toggles:
        Application.action("erase_action").setChecked(False)
    Application.action("preserve_alpha").trigger()


def is_alpha_locked():
    'returns True if the alpha is locked'
    krita_preserve_alpha_action = Application.action("preserve_alpha")
    return krita_preserve_alpha_action.isChecked()
