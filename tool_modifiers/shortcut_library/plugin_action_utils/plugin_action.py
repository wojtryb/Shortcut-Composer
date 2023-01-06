from dataclasses import dataclass


@dataclass
class PluginAction:
    """
    Abstract class with custom key event interface

    Child class can specify what to do on any of given callbacks:

    - on_key_press
    - on_short_key_release
    - on_long_key_release
    - on_every_key_release
    """

    action_name: str

    def __pre_init__(self):
        self.time_interval: float

    def on_key_press(self):
        """Called on each press of key specified in settings."""

    def on_long_key_release(self):
        """Called when related key was released after a long time."""

    def on_short_key_release(self):
        """Called when related key was released shortly after press."""

    def on_every_key_release(self):
        """Called on each release of related key, after short/long callback."""
