# Shortcut composer

**Extension** for painting application **Krita**, which allows to create custom, complex **keyboard shortcuts**.


The plugin adds new shortcuts of the following types:
- `Mouse tracker` - while key is pressed, tracks a mouse, switching values according to cursor offset.
- `Preview` - displays on-canvas preview while the key is pressed.
- `Multiple assignment` - repeatedly pressing a key cycles between multiple values of krita property.
- `Temporary key` - temporarily activates a krita property with long press or toggles it on/off with a short one.

## Installation:
1. on [github project page](https://github.com/wojtryb/Shortcut-Composer), click the green button <kbd>code</kbd> and pick the <kbd>download zip</kbd> option. Do not extract it.
2. in krita's topbar, open **Tools > Scripts > Import Python Plugin From File** and pick the downloaded .zip file
3. restart krita.
4. set custom shortcuts in **Settings > Configure Krita > Keyboard Shortcuts** under **Scripts > Shortcut Composer** section. By intention, there are no default bindings.

<!-- Screen z akcjami w Keyboard Shortcuts -->

## Pre-made actions
Shortcut composer add-on comes with multiple pre-made, highly configurable and extendable actions which can be used out-of-the-box.

### (`Mouse tracker`): Scroll isolated layers
Used for picking layers and analizing the layer stack. Scrolls all active layer by sliding the cursor vertically. While the action is running, isolates active layer.

<!-- <img src="https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif" width="120" height="40" /> -->

### (`Mouse tracker`): Scroll timeline or animated layers
Variation on "Scroll isolated layers" for animators. Layers are restricted only to animated ones. Horizontal mouse movement changes current frame on the timeline.

### (`Mouse tracker`): Scroll undo stack
Extends the usual undo(<kbd>ctrl</kbd>+<kbd>z</kbd>) action. Controls the undo stack by sliding the cursor horizontally. Usual undoing is still possible.

### (`Mouse tracker`): Scroll brush size or opacity
Allows to control both `brush size` and `opacity` with single key. Opacity changes contiguously with vertical mouse movement, while brush size snaps to custom values. It is meant to provide easy access to precise values for pixel artists.

### (`Preview`): Preview current layer visibility
Changes active layer visibility on key press and release. Allows to quickly check layer's content.

### (`Preview`): Preview projection below
Hides all visible layers above the active one on key press, and reverses this action on key release. Allows to check what is the position of current layer in a stack. It is possible to paint while the key is pressed and layers above are temporarily hidden.

### (`Multiple assignment`): Cycle selection tools
Pressing a key repeatedly cycles most commonly used selection tools:
- `freehand selection tool`,
- `rectangular selection tool`,
- `contiguous selection tool`

Performing a long press, goes back to the `freehand brush tool`. Tools can be used while the key is pressed.

### (`Multiple assignment`): Cycle misc tools
Pressing a key repeatedly cycles most commonly used miscellaneous tools:
- `crop tool`,
- `reference tool`,
- `gradient tool`,
- `multi_brush tool`

Performing a long press, goes back to the `freehand brush tool`. Tools can be used while the key is pressed.

### (`Multiple assignment`): Cycle painting opacity
Pressing a key repeatedly cycles brush predefined opacity values: `100%`, `70%`, `50%`, `30%`
Performing a long press, goes back to the `100%` opacity. Modified opacity can be used while the key is pressed.

### (`Multiple assignment`): Cycle painting blending modes
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

### (`Multiple assignment`): Cycle brush presets
Pressing a key repeatedly cycles brush presets from default `"Digital"` tag. Used tag is configurable.

### (`Temporary key`): Temporary move tool
Pressing a key temporarily activates the `move tool` which goes back to the `freehand brush tool` after the key release. Short key presses allow to permanently toggle between those two tools. Allows to move elements faster. 

### (`Temporary key`): Temporary transform tool
Pressing a key temporarily activates the `transform tool` which goes back to the `freehand brush tool` after the key release. Short key presses allow to permanently toggle between those two tools. Allows to perform basic transformations faster. Other modes require permanent toggling.

### (`Temporary key`)Temporary eraser
Pressing a key temporarily activates the `eraser` mode which gets turned off after the key release. Short key presses allow to permanently toggle between those two states. 

### (`Temporary key`): Temporary preserve alpha
Pressing a key temporarily activates the `preserve alpha` mode which gets turned off after the key release. Short key presses allow to permanently toggle between those two states. 

## Configuration and creating custom actions
- in krita's topbar, open **Settings > Manage Resources > Open Resource Folder**
- navigate to **./pykrita/shortcut_composer/** directory.
- action definitions are located in `shortcut_composer.action` file.
- action implementation is located in `actions.py` file.

To change actions name or create a new one, both files need to be edited. Make sure that the names in respective files matches. Note that changing the implementation may require basic understanding of python syntax. For programming hints, check docstrings of python classes.

## Worth noting
- Key bindings with modifiers like <kbd>ctrl</kbd> or <kbd>shift</kbd> are supported. In this case the key is considered released when the main key in sequence (non-modifier) is released.
- Multiple shortcuts from this plugin can be used at the same time, unless bindings make it technically impossible. For example holding both keys for `Temporary eraser` and `Cycle painting opacity` result in an eraser with 70% opacity.

## Known limitations
- Pressing a modifier while the usual key is pressed, will result in conflict. For instance, pressing <kbd>ctrl</kbd> while using temporary eraser assigned to <kbd>x</kbd> will result in unwanted <kbd>ctrl</kbd>+<kbd>x</kbd> operation which cuts current layer.
- Controllers for setting canvas `zoom`, `rotation` and `active presets` cannot be used with `Mouse tracker` template which needs to utilize different threads. 

## For krita plugin programmers
The extension consists of elements that can be reused in other krita plugins under GPL3 license.

### Alternative API
Package `api_krita` consists of wrapper for krita api. It offers PEP8 compatibility, typings, and docstrings.

Most of objects attributes are now rewritten as settables properties 

Copy `api_krita` to the extension directory, to access syntax such as:
```python
from .api_krita import Krita
from .api_krita.enums import BlendingMode, Tool, Toggle

# active tool operations
tool = Krita.active_tool  # get current tool
Krita.active_tool = Tool.FREEHAND_BRUSH  # set current tool
Tool.FREEHAND_BRUSH.activate()  # set current tool (alternative way)

# operations on a document
document = Krita.get_active_document()
all_nodes = document.get_all_nodes()  # all nodes with flattened structure
picked_node = all_nodes[3]

picked_node.name = "My layer name"
picked_node.visible = True
picked_node.opacity = 50  # remapped from 0-255 go 0-100 [%]
document.active_node = picked_node 
document.refresh()

# Operations on a view
view = Krita.get_active_view()
view.brush_size = 100
view.blending_mode = BlendingMode.NORMAL  # Enumerated blending modes

# Handling checkable actions
mirror_state = Toggle.MIRROR_CANVAS.state  # get mirror state
Toggle.SOFT_PROOFING.state = False  # turn off soft proofing
Toggle.PRESERVE_ALPHA.switch_state()  # change state of preserve alpha

```

### Custom keyboard shortcut interface
Package `input_adapter` consists of `ActionManager` and `PluginAction` which grant extended interface for creating keyboard shortcuts.

While usual actions can only recognise key press, subclassing `PluginAction` lets you override methods performed on:
- key press
- short key release
- long key release
- every key release

Then use `ActionManager` instance to bind objects of those custom actions to krita during CreateActions phase:

```python
class ExtensionName(Extension):
    ...
    def createActions(self, window) -> None:
        action = PluginActionChild(name="...")
        self.manager = ActionManager(window)
        self.manager.bind_action(action)
```
