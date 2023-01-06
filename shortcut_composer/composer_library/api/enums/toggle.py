from enum import Enum


class Toggle(Enum):
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
