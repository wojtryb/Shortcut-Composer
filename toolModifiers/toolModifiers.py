from functools import partial
from krita import Krita, Extension

from .importCode.event_filter import ReleaseKeyEventFilter
from .importCode.action_wrapper import ActionCreator
from .importCode.pass_functions import (
    set_tool,
    is_tool_selected,
    is_eraser_active,
    toggle_eraser,
    is_alpha_locked,
    toggle_alpha_lock)

from .config import tools


class toolModifiers(Extension):
    'the extension'

    def __init__(self, parent):
        super(toolModifiers, self).__init__(parent)
        self.actions = []
        self.event_filter = ReleaseKeyEventFilter()

    def setup(self):
        pass

    def createActions(self, window):
        """
        run on startup - creates all keyboard shortcuts in the plugin - tool
        modifiers needed by the user, and toggles for eraser and preserve alpha
        """
        creator = ActionCreator(window)

        for human_name, krita_name in tools.items():
            action = creator.create_shortcut(
                human_name=human_name,
                set_low_function=partial(set_tool, "KritaShape/KisToolBrush"),
                set_high_function=partial(set_tool, krita_name),
                is_high_state_function=partial(is_tool_selected, krita_name)
            )
            self.event_filter.register_release_callback(
                action.shortcut.event_filter_callback)
            self.actions.append(action)

        # 'create action for eraser'
        action = creator.create_shortcut(
            human_name='Eraser (toggle)',
            set_low_function=toggle_eraser,
            set_high_function=toggle_eraser,
            is_high_state_function=is_eraser_active
        )
        self.event_filter.register_release_callback(
            action.shortcut.event_filter_callback)
        self.actions.append(action)

        # 'create action for alpha lock'
        action = creator.create_shortcut(
            human_name='Preserve alpha (toggle)',
            set_low_function=toggle_alpha_lock,
            set_high_function=toggle_alpha_lock,
            is_high_state_function=is_alpha_locked
        )
        self.event_filter.register_release_callback(
            action.shortcut.event_filter_callback)
        self.actions.append(action)


Krita.instance().addExtension(toolModifiers(Krita.instance()))
