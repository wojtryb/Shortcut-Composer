### Custom keyboard shortcut interface
Package `input_adapter` consists of `ActionManager` and `ComplexActionInterface` which together allow to recognize more keyboard events than usual krita action does.

While usual actions can only recognize key press, implementing `ComplexActionInterface` lets you override methods performed on:
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