### Alternative Krita API
Package `api_krita` wraps krita api offering PEP8 compatibility, typings, and docstring documentation. Most of objects attributes are now available as settable properties.

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
