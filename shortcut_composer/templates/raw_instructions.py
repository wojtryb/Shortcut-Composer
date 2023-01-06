# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from input_adapter import ComplexAction


class RawInstructions(ComplexAction):
    """
    Temporarily toggle plugin instructions.

    Action starts all the instructions on key press, and ends them on
    release.

    ### Arguments:

    - `name`         -- unique name of action. Must match the definition
                        in shortcut_composer.action file
    - `instructions` -- (optional) list of additional instructions to
                        perform on key press and release.
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long.

    ### Action implementation example:

    Example action is meant to turn on ISOLATE_LAYER action for as long
    as the key is pressed.

    ```python
    templates.RawInstructions(
        name="Toggle isolate layer (temporary)",
        instructions=[
            instructions.TemporaryOn(Toggle.ISOLATE_LAYER)
        ],
        short_vs_long_press_time=0.3
    )
    ```
    """
