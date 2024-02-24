# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from krita import Krita as Api


class Toggle(Enum):
    """
    Contains all known actions that toggle (can be activated and deactivated).

    Example usage: `Toggle.ERASER`
    """

    ERASER = "erase_action"
    PRESERVE_ALPHA = "preserve_alpha"
    MIRROR_CANVAS = "mirror_canvas"
    SOFT_PROOFING = "softProof"
    ISOLATE_LAYER = "isolate_active_layer"
    VIEW_REFERENCE_IMAGES = "view_toggle_reference_images"
    VIEW_ASSISTANTS = "view_toggle_painting_assistants"
    VIEW_ASSISTANTS_PREVIEWS = "view_toggle_assistant_previews"
    VIEW_GRID = "view_grid"
    VIEW_RULER = "view_ruler"
    VIEW_ONION_SKIN = "toggle_onion_skin"
    SNAP_ASSISTANT = "toggle_assistant"
    SNAP_TO_GRID = "view_snap_to_grid"

    @property
    def pretty_name(self) -> str:
        """Format toggle name like: `Preserve alpha`."""
        return f"{self.name.replace('_', ' ').capitalize()}"

    @property
    def state(self) -> bool:
        """Return state of checkable krita action called `action_name`."""
        return Api.instance().action(self.value).isChecked()

    @state.setter
    def state(self, state: bool) -> None:
        """Set state of checkable krita action (toggle) by its enum."""
        return Api.instance().action(self.value).setChecked(state)

    def switch_state(self) -> None:
        """Change state from ON to OFF and vice-versa."""
        self.state = not self.state
