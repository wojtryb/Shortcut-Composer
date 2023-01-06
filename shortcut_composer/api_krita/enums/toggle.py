# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from enum import Enum


class Toggle(Enum):
    """
    Contains all known actions that toggle (can be activated and deactivated).

    Example usage: `Toggle.ERASER`

    Available toggle actions:
    - `ERASER`
    - `PRESERVE_ALPHA`
    - `MIRROR_CANVAS`
    - `SOFT_PROOFING`
    - `ISOLATE_LAYER`
    - `VIEW_REFERENCE_IMAGES`
    - `VIEW_ASSISTANTS`
    - `VIEW_ASSISTANTS_PREVIEWS`
    - `VIEW_GRID`
    - `VIEW_RULER`
    - `VIEW_ONION_SKIN`
    - `SNAP_ASSISTANT`
    - `SNAP_TO_GRID`
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
