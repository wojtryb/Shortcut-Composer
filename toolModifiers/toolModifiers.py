from krita import *

from .importCode.action_wrapper import ActionCreator
from .importCode.passFunctions import (
    setTool,
    setBrushTool,
    isToolSelected,
    isEraserActive,
    toggleEraser,
    isAlphaLocked,
    toggleAlphaLock)
from .importCode.definedActions import definedActions

from .SETUP import TOOLS


class toolModifiers(Extension):
    'the extension'

    def __init__(self, parent):
        super(toolModifiers, self).__init__(parent)
        self.actions = []

    def setup(self):
        pass

    def createActions(self, window):
        """
        run on startup - creates all keyboard shortcuts in the plugin - tool
        modifiers needed by the user, and toggles for eraser and preserve alpha
        """
        creator = ActionCreator(window)
        i = 1

        # 'create an action for each of the tool toggle shortcuts'
        for krita_name in TOOLS:
            human_name = definedActions.get(krita_name, f'Tool {i} (toggle)')
            if human_name.split(" ")[0] == "Tool":
                i += 1

            self.actions.append(creator.create_shortcut(
                human_name=human_name,
                krita_name=krita_name,
                set_low_function=setBrushTool,
                set_high_function=setTool,
                is_high_state_function=isToolSelected
            ))

        # 'create action for eraser'
        self.actions.append(creator.create_shortcut(
            'Eraser (toggle)',
            '',
            toggleEraser,
            toggleEraser,
            isEraserActive
        ))

        # 'create action for alpha lock'
        self.actions.append(creator.create_shortcut(
            'Preserve alpha (toggle)',
            '',
            toggleAlphaLock,
            toggleAlphaLock,
            isAlphaLocked
        ))


# 'load the extension on krita start-up'
Krita.instance().addExtension(toolModifiers(Krita.instance()))
