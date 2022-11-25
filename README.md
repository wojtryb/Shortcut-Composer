# Shortcut composer

Extension for painting application Krita, which allows to create custom, complex keyboard shortcuts.

Add-on comes with multiple pre-made, highly configurable and extendable actions which can be used out-of-the-box.

The plugin adds new shortcuts of the following types:
- `Temporary key` - temporarily activates a krita property with long press or toggles it on and off with a short press.
- `Multiple assignment` - repeatedly pressing a key cycles between multiple values of krita property.
- `Mouse tracker` - while key is pressed, tracks a mouse along given axis, switching values according to cursor offset.
- `Preview` - displays on-canvas preview while the key is pressed.

## Installation:
- on [github project page](https://github.com/wojtryb/Shortcut-Composer), click the green button `code` and pick the `download zip` option. Do not extract it.
- in krita's topbar, open `Tools > Scripts > Import Python Plugin From File` and pick the downloaded .zip file
- restart krita.
- set custom shortcuts in `Settings > Configure Krita > Keyboard Shortcuts` under `Scripts > Shortcut Composer` section. By intention, there are no default bindings.

## Pre-made actions

### Scroll isolated layers (`Mouse tracker`)
Used for picking layers and analizing the layer stack. Scrolls all active layer by sliding the cursor vertically. While the action is running, isolates active layer.

<!-- <img src="https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif" width="120" height="40" /> -->

### Scroll timeline or animated layers (`Mouse tracker`)
Variation on "Scroll isolated layers" for animators. Layers are restricted only to animated ones. Horizontal mouse movement changes current frame on the timeline.

### Scroll undo stack (`Mouse tracker`)
Extends the usual undo(`ctrl+z`) action. Controls the undo stack by sliding the cursor horizontally. Undoing is still possible with short key presses.

### Scroll brush size or opacity (`Mouse tracker`)
Allows to control both `brush size` and `opacity` with single key. Opacity changes contiguously with vertical mouse movement, while brush size snaps to custom values. It is meant to provide easy access to precise values for pixel artists.

### Preview current layer visibility (`Preview`)
Changes active layer visibility on key press and release. Allows to quickly check layer's content.

### Preview projection below (`Preview`)
Hides all visible layers above the active one on key press, and reverses this action on key release. Allows to check what is the position of current layer in a stack. It is possible to paint while the key is pressed and layers above are temporarily hidden.

### Cycle selection tools (`Multiple assignment`)
Pressing a key repeatedly cycles most commonly used selection tools:
- `freehand selection tool`,
- `rectangular selection tool`,
- `contiguous selection tool`

Performing a long press, goes back to the `freehand brush tool`. Tools can be used while the key is pressed.

### Cycle misc tools (`Multiple assignment`)
Pressing a key repeatedly cycles most commonly used miscellaneous tools:
- `crop tool`,
- `reference tool`,
- `gradient tool`,
- `multi_brush tool`

Performing a long press, goes back to the `freehand brush tool`. Tools can be used while the key is pressed.

### Cycle painting opacity (`Multiple assignment`)
Pressing a key repeatedly cycles brush predefined opacity values: `100%`, `70%`, `50%`, `30%`
Performing a long press, goes back to the `100%` opacity. Modified opacity can be used while the key is pressed.

### Cycle painting blending modes (`Multiple assignment`)
Pressing a key repeatedly cycles most commonly used blending modes:
- `overlay`,
- `multiply`,
- `color`,
- `add`,
- `behind`,
- `darken`,
- `lighten`,
- `normal`,

Performing a long press, goes back to the `normal` mode. Modified mode can be used while the key is pressed.

### Cycle brush presets (`Multiple assignment`)
Pressing a key repeatedly cycles brush presets from default `"Digital"` tag. Used tag is configurable.

### Temporary move tool (`Temporary key`)
Pressing a key temporarily activates the `move tool` which goes back to the `freehand brush tool` after the key release. Short key presses allow to permanently toggle between those two tools. Allows to move elements faster. 

### Temporary transform tool (`Temporary key`)
Pressing a key temporarily activates the `transform tool` which goes back to the `freehand brush tool` after the key release. Short key presses allow to permanently toggle between those two tools. Allows to perform basic transformations faster. Other modes require permanent toggling.

### Temporary eraser (`Temporary key`)
Pressing a key temporarily activates the `eraser` mode which gets turned off after the key release. Short key presses allow to permanently toggle between those two states. 

### Temporary preserve alpha (`Temporary key`)
Pressing a key temporarily activates the `preserve alpha` mode which gets turned off after the key release. Short key presses allow to permanently toggle between those two states. 

## Configuration and creating custom actions
- in krita's topbar, open `Settings > Manage Resources > Open Resource Folder`
- navigate to `./pykrita/shortcut_composer/` directory.
- action definitions are located in `shortcut_composer.action` file.
- action implementation is located in `actions.py` file.

To change actions name or create a new one, both files need to be edited. Make sure that the names in respective files matches. Note that changing the implementation may require basic understanding of python syntax. For programming hints, check docstrings of python classes.

## Worth noting
- Key bindings with modifiers like `ctrl` or `shift` are supported. In this case the key is considered released when the main key in sequence (non-modifier) is released.
- Multiple shortcuts from this plugin can be used at the same time, unless bindings make it technically impossible. For example holding both keys for `Temporary eraser` and `Cycle painting opacity` result in an eraser with 70% opacity.

## Known limitations
- Pressing a modifier while the usual key is pressed, will result in conflict. For instance, pressing `ctrl` while using temporary eraser assigned to `x` will result in unwanted `ctrl+x` operation which cuts current layer.
- Controllers for setting canvas `zoom`, `rotation` and `active presets` cannot be used with `Mouse tracker` template which needs to utilize different threads. 
