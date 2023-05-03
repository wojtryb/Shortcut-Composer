# Shortcut composer

**Extension** for painting application **Krita**, which allows to create custom, complex **keyboard shortcuts**.

The plugin adds new shortcuts of the following types:
- `Pie menu` - while key is pressed, displays a pie menu, which allows to pick values by hovering a mouse.
- `Cursor tracker` - while key is pressed, tracks a cursor, switching values according to cursor offset.
- `Canvas preview` - Temporarily changes canvas elements while the key is pressed.
- `Multiple assignment` - repeatedly pressing a key, cycles between multiple values of krita property.
- `Temporary key` - temporarily activates a krita property with long press or toggles it on/off with short press.

## What's new in **1.2**

[![PIE MENUS - introducing Shortcut Composer](http://img.youtube.com/vi/Tkf2-U0OyG4/0.jpg)](https://www.youtube.com/watch?v=Tkf2-U0OyG4 "PIE MENUS - introducing Shortcut Composer")

- [hotfix **1.2.2**] - Fixed MultipleAssignment actions sharing one configuration window.
- [hotfix **1.2.1**] - Fixed pie menus in edit mode hiding when clicked outside on the canvas.


### Added
- Adding and removing PieMenu icons with drag and drop.
- Class-oriented configuration system with automatic value parsing. Can be reused in other plugins. 
- PieMenus are now able to handle their own local configuration with Pie settings (Replaces section in `Configure Shortcut Composer`).
- Change PieIcon border's color when hovered in EditMode (Replaces gray indicator)
- Allow changes to PieMenu and PieIcon size for each pie separately.
- Separate button to enter PieMenu edit mode. Replaces clicking on PieIcon which was easy to do unintentionally.
- Preset PieMenus tag now can be chosen directly from the Pie settings. (Replaces section in `Configure Shortcut Composer`)
- Preset PieMenus now reload automatically when the tag content changes. (Replaces `Reload Shortcut Composer` action)
- PieMenus now automatically change between dark/light theme when the krita theme changes between these two theme families.
- `Cycle selection tools` action now is configured by local settings activated with a button that appears on long press (Replaces section in `Configure Shortcut Composer`)

### Fixed
- Support tags with quote and double-quote signs.
- Make `input_adapter` package independent from the rest of the plugin to improve re-usability.
- Fix crash when picking a deleted preset with PieMenu.

Check out historic [changelogs](https://github.com/wojtryb/Shortcut-Composer/releases).

## Plugin release video:

[![PIE MENUS - introducing Shortcut Composer](http://img.youtube.com/vi/hrjBycVYFZM/0.jpg)](https://www.youtube.com/watch?v=hrjBycVYFZM "PIE MENUS - introducing Shortcut Composer")

## Requirements
- Version of krita on plugin release: **5.1.5**
- Required version of krita: **5.1.0**

OS support state:
- [x] Windows (10, 11)
- [x] Linux (Ubuntu 20.04, 22.04)
- [ ] MacOS (Known bug of canvas losing focus after using PieMenu)
- [ ] Android (Does not support python plugins yet)

> **Note**
> On **Linux** the only oficially supported version of Krita is **.appimage**, which ships with all required dependencies. Running the plugin on Krita installed from Snap or distribution repositories is not recommended as it may not work out of the box and may require extra dependency-related work.  

## How to install or update the plugin:
1. on [github project page](https://github.com/wojtryb/Shortcut-Composer), click the green button <kbd>code</kbd> and pick the <kbd>download zip</kbd> option. Do not extract it.
2. in krita's topbar, open **Tools > Scripts > Import Python Plugin From File** and pick the downloaded .zip file
3. restart krita.
4. set custom shortcuts in **Settings > Configure Krita > Keyboard Shortcuts** under **Scripts > Shortcut Composer: Complex Actions** section. By intention, there are no default bindings.

> **Warning**
> Some keyboard buttons like **Space, R, Y, V, 1, 2, 3, 4, 5, 6** are reserved for Krita's Canvas Inputs. Assigning those keys to actions (including those from the plugin) may result in conflicts and abnormal behaviour different for each OS. Either avoid those keys, or remove their bindings in **Settings > Configure Krita > Canvas Input Settings**.

## Pre-made actions
While Shortcut-Composer is highly configurable and extendable, the add-on comes with pre-made, plug-and-play actions.

### (`Pie menus`):
Pie menu is a widget displayed on the canvas while a key is pressed. It will disappear as soon, as the key is released. Moving cursor in a direction of an icon, activates its value on key release. **The action only requires hovering**. Pie menu does nothing if the cursor is not moved out of the deadzone.

Clicking the settings button in bottom-right corner switches into `Edit mode` which allows to modify pie. At this point the keyboard button no longer needs to be pressed. In this mode values one can:
- drag icons to change their order
- drag icons out of the ring to remove them
- drag icons from the settings window to add them

Settings window visible in `Edit mode` also allows to change the local settings of the pie. When done, press the tick button to apply the changes. 

- ### Pick brush presets (red, green, blue)
  Three color coded pie menus that let you pick a **brush preset** from related **tag** with brush presets.
  
  Used tag can be changed in pie settings by entering `Edit mode`. Presets in the pie depend on the tag, so they cannot be removed or added with dragging, but it is possible to change their order. When presets are added or remove from the tag, pie should update automatically.
  
  Default tag mapping is as follows:
  - <span style="color:red">red</span>: "★ My Favorites"
  - <span style="color:green">green</span>: "RGBA"
  - <span style="color:blue">blue</span>: "Erasers"

- ### Pick misc tools
  Pie menu for picking **active tools**. It is recommended to change the default values being:
  - crop tool,
  - reference tool,
  - gradient tool,
  - multi_brush tool,
  - assistant tool
  
- ### Pick painting blending modes
  Pie menu for picking **painting blending modes**. It is recommended to change the default values being:
  - normal
  - overlay,
  - color,
  - multiply,
  - add,
  - screen,
  - darken,
  - lighten

- ### Create painting layer with blending mode
  Pie menu for creating a new layer with picked **blending mode**. It is recommended to change the default values being:
  - normal
  - erase
  - overlay,
  - color,
  - multiply,
  - add,
  - screen,
  - darken,
  - lighten
  
### (`Cursor trackers`):
Cursor tracker is an action for switching values using cursor movement, while the keyboard key is pressed. It changes a single krita property according to the cursor movement along horizontal or vertical axis. **The action does not recognise mouse clicks, and only requires hovering**

- ### Scroll isolated layers
  Scrolls the layers by sliding the cursor vertically. Can be used for picking the active layer and analizing the layer stack. While the key is pressed, isolates the active layer to give better response of which layer is active.
  - Key press: isloate active layer
  - Horizontal: -
  - Vertical: scroll all layers

- ### Scroll timeline or animated layers
  Variation on "Scroll isolated layers" for animators. Scrolling is restricted only to layers pinned to the animation timeline. Horizontal mouse movement changes the current frame.
  - Key press: isloate active layer
  - Horizontal: scroll animation frames
  - Vertical: scroll layers pinned to timeline

- ### Scroll undo stack
  Extends the krita undo action <kbd>ctrl</kbd>+<kbd>z</kbd>. While the key is pressed, horizontal mouse movement controls the undo stack by performing undo and redo actions. Usual undo with short key press is still possible.
  - Key press: undo last operation
  - Horizontal: scroll left to undo, or right to redo
  - Vertical: -

- ### Scroll brush size or opacity
  Allows to control both `brush size` or `opacity` with a single key. Opacity changes contiguously with vertical mouse movement, while brush size snaps to custom values.
  - Key press: -
  - Horizontal: scroll brush size (descrete)
  - Vertical: scroll painting opacity (contiguous)

- ### Scroll canvas zoom or rotation
  Allows to control both `canvas zoom` or `canvas rotation` with a single key. Does not block the ability to paint.
  - Key press: -
  - Horizontal: canvas rotation (contiguous)
  - Vertical: canvas zoom (contiguous)

### (`Canvas previews`):
Canvas preview is an action which changes canvas elements when the key is pressed, and changes them back to their original state on key release.

- ### Preview current layer visibility
  Changes active layer visibility on key press and release. Allows to quickly check layer's content.

- ### Preview projection below
  Hides all visible layers above the active one on key press, and reverses this change on key release. Allows to check what is the position of current layer in a stack. It is possible to paint while action is active.

### (`Multiple assignments`):
Multiple assignment is an action which cycles between multiple values of single krita property. Each key press activates next list element. Performing a long press breaks the cycle and sets a default value, which does not have to belong the the list.

- ### Cycle selection tools
  Pressing a key repeatedly cycles most commonly used selection tools:
  - freehand selection tool,
  - rectangular selection tool,
  - contiguous selection tool

  Performing a long press, goes back to the `freehand brush tool`. Tools can be used while the key is pressed.

  Default values can be modified in `Edit mode`. To enter it, long press the button, and click on the button which appears in top-left corner of painting area.

  Values are added by selecting the list value(s) on the left and pressing the green **add** button. Analogically, selecting values on the right, and pressing the **remove** button, removes the values from action. Dragging values on the right, allow to change their order.

- ### Cycle painting opacity
  Pressing a key repeatedly cycles brush predefined opacity values: `100%`, `70%`, `50%`, `30%`

  Performing a long press, goes back to the `100%` opacity. Modified opacity can be used while the key is pressed.

  Currently does not allow to configure predefined values without editing code.

### (`Temporary keys`):
- ### Temporary move tool
  Pressing a key temporarily activates the `move tool` which goes back to the `freehand brush tool` after the key release. Short key presses allow to permanently toggle between those two tools. 

- ### Temporary eraser
  Pressing a key temporarily activates the `eraser` mode which gets turned off after the key is released. Short key presses allow to permanently toggle between those two states. 

- ### Temporary preserve alpha
  Pressing a key temporarily activates the `preserve alpha` mode which gets turned off after the key is released. Short key presses allow to permanently toggle between those two states. 

## Modifying default plugin behaviour

### Tweaking the global parameters
Shortcut-Composer comes with a settings dialog available from krita topbar: **Tools > Scripts > Configure Shortcut Composer**. The dialog allows to change the following aspects of actions:

- Common settings
  - `Short vs long press time` - Time in seconds distinguishing short key presses from long ones.
  - `FPS limit` - Maximum rate of Mouse Tracker and Pie Menu refresh.
- Cursor trackers
  - `Tracker sensitivity scale` - Sensitivity multiplier of all Mouse Trackers. 
  - `Tracker deadzone` - Amount of pixels a mouse needs to moved for Mouse Trackers to start work.
- Pie menus display
  - `Pie global scale` - Global scale factor for base of every pie menu.
  - `Pie icon global scale` - Global scale factor for icons of every pie menu.
  - `Pie deadzone global scale` - Global scale factor for the deadzone area of every pie menu.
  - `Pie animation time` - Time (in seconds) for fade-in animation when showing the pie menu.

### Modifying actions and creating custom ones
While the settings dialog allows to tweak the values common for plugin actions, it does not allow to modify the behaviour of the actions or create new ones.

To achieve that it is required to modify actions implementation: 
- in krita's topbar, open **Settings > Manage Resources > Open Resource Folder**
- navigate to **./pykrita/shortcut_composer/** directory.
- action definitions are located in `actions.action` file.
- actions implementation is located in `actions.py` file.

1. Define an action in `actions.action` file by duplicating one of the existing definitions and using an unique name for it.
2. Implement an action in `actions.py` file. Once again, duplicate one of the existing implementations. It is best to pick the one that feels closest to desired action. Fill its arguments, making sure the name is exactly the same as defined earlier.
 
## Worth noting
- Key bindings with modifiers like <kbd>ctrl</kbd> or <kbd>shift</kbd> are supported. When assigned to a key combination, the key is considered released when the main key in sequence (non-modifier) is released.
- Multiple shortcuts from this plugin can be used at the same time, unless bindings make it technically impossible. For example holding both keys for `Temporary eraser` and `Cycle painting opacity` result in an eraser with 70% opacity.

### Known limitations
- Pressing a modifier while the usual key is pressed, will result in conflict. For instance, pressing <kbd>ctrl</kbd> while using temporary eraser assigned to <kbd>x</kbd> will result in unwanted <kbd>ctrl</kbd>+<kbd>x</kbd> operation which cuts current layer.
- It is possible to activate multiple pie menus at the same time.
- Keyboard shortcuts assigned to actions can conflict with Canvas Input (General limitation of Krita).

## For krita plugin programmers
Some parts of plugin code solve general problems, which can apply outside of Shortcut Composer. Those solutions were placed in separate packages that can be copy-pasted into any other plugin and reused there.

They depend only on original Krita API and PyQt5 with which krita is shipped.

### Custom keyboard shortcut interface
Package `input_adapter` consists of `ActionManager` and `ComplexActionInterface` which together allow to recognise more keyboard events than usual krita action does.

While usual actions can only recognise key press, implementing `ComplexActionInterface` lets you override methods performed on:
- key press
- short key release
- long key release
- every key release

Each action needs to have public `name: str` attribute which is the same, as the one used in .action file, as well as `short_vs_long_press_time: float` which determines how many seconds need to elapse to consider that a key press was long.

Use `ActionManager` instance to bind objects of those custom actions to krita during `CreateActions` phase:

```python
"""
Print whether action key was released before of after
0.2 seconds from being pressed.
"""
from krita import Krita
from input_adapter import ActionManager, ComplexActionInterface


class CustomAction(ComplexActionInterface):
    def __init__(self, name: str, press_time: float = 0.2):
      self.name = name
      self.short_vs_long_press_time = press_time

    def on_key_press(self): print("key was pressed")
    def on_short_key_release(self): print("key released before than 0.2s")
    def on_long_key_release(self): print("key released later than after 0.2s")
    def on_every_key_release(self): pass


class MyExtension(Extension):
    def setup(self) -> None: pass
    def createActions(self, window) -> None:
        action = CustomAction(name="Custom action name")
        self.manager = ActionManager(window)
        self.manager.bind_action(action)

Krita.instance().addExtension(MyExtension(Krita.instance()))
```

### Config system
Package `config_system` consists of `Field` and `FieldGroup` which grant object-oriented API to control kritarc configuration file easier, than with API of krita.

---

`Field` represents a single value in kritarc file. Once initialized with its group name, name and default value, it allows to:
- write a given value to kritarc.
- read current value from kritarc, parsing it to correct python type.
- reset the value to default.
- register a callback run on each value change.

Type of default value passed on initlization is remembered, and used to parse values both on read and write. Supported types are:
- `int`, `list[int]`,
- `float`, `list[float]`,
- `str`, `list[str]`,
- `bool`, `list[bool]`,
- `Enum`, `list[Enum]`

For empty, homogeneous lists, `parser_type` argument must be used to determine type of list elements. Default values are not saved when until the field does not exist in kritarc. Repeated saves of the same value are filtered, so that callbacks are not called when the same value is written multiple times one after the other.

---

`FieldGroup` represents a section of fields in kritarc file. It simplifies the field creation by auto-completing the group name.

FieldGroup holds and aggregates fields created with it. It allows to reset all the fields at once, and register a callback to all its fields: both existing and future ones.

---

Example usage:
```python
from enum import Enum
from config_system import FieldGroup


class EnumMock(Enum):
    MODE_A = 0
    MODE_B = 1

# Create a config group
group = FieldGroup("MyGroup")
# Register a callback on all three fields
group.register_callback(lambda: print("any field changed"))

# Create three fields inside a group - for string and two enum lists
str_field = group.field(name="my_str", default="Sketch")
enums_field_1 = group.field("my_enums_1", [], parser_type=EnumMock)
enums_field_2 = group.field("my_enums_2", [EnumMock.MODE_A])

# Register a different callback on each field
str_field.register_callback(lambda: print("string changed"))
enums_field_1.register_callback(lambda: print("enum 1 changed"))
enums_field_2.register_callback(lambda: print("enum 2 changed"))

# Change the value from default "Sketch" to "Digital"
str_field.write("Digital")
# Change the value from empty list to one with two values
enums_field_1.write([EnumMock.MODE_A, EnumMock.MODE_B])
# Repeat the default value. Will be filtered
enums_field_2.write([EnumMock.MODE_A])

# The program will not break, as red values are the same as written ones
assert str_field.read() == "Digital"
assert enums_field_1.read() == [EnumMock.MODE_A, EnumMock.MODE_B]
assert enums_field_2.read() == [EnumMock.MODE_A]
```

The code above produces "MyGroup" section in kritarc file. my_enums_2 is missing, as the default value was not changed:
```
[MyGroup]
my_str=Digital
my_enums_1=MODE_A\tMODE_B
```

Registered callbacks outputs on the terminal:
```
any field changed
string changed
any field changed
enum 1 changed
```

Calling `group.reset_defaults()` would change both values back to their defaults, and produce the same output on the terminal, as resetting changes the fields.

### Alternative API
Package `api_krita` wraps krita api offering PEP8 compatibility, typings, and docstring documentation. Most of objects attributes are now available as settables properties.

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

Only functionalities that were needed during this plugin development are wrapped, so some of them are not yet available. The syntax can also change over time.
