from dataclasses import dataclass
from typing import Any

from PyQt5.QtWidgets import QWidget, QToolButton
from krita import Krita as Api, Extension, QMdiArea


@dataclass
class KritaView:

    view: Any

    def current_brush_preset_name(self) -> str:
        return self.view.currentBrushPreset().name()

    def current_blending_mode(self):
        return self.view.currentBlendingMode()

    def current_opacity(self) -> int:
        return self.view.paintingOpacity()

    def set_brush_preset(self, preset_name: str):
        self.view.setCurrentBrushPreset(preset_name)

    def set_blending_mode(self, mode_name: str):
        self.view.setCurrentBlendingMode(mode_name)

    def set_opacity(self, opacity: int) -> None:
        self.view.setPaintingOpacity(opacity)


class Krita:
    @staticmethod
    def trigger_action(action_name) -> None:
        return Api.instance().action(action_name).trigger()

    @staticmethod
    def get_action_shortcut(action_name: str) -> str:
        return Api.instance().action(action_name).shortcut()

    @staticmethod
    def get_action_state(action_name: str) -> bool:
        return Api.instance().action(action_name).isChecked()

    @staticmethod
    def set_action_state(action_name: str, state: bool) -> None:
        return Api.instance().action(action_name).setChecked(state)

    @staticmethod
    def get_presets() -> list:
        return Api.instance().resources('preset')

    @staticmethod
    def get_active_view() -> KritaView:
        return KritaView(Api.instance().activeWindow().activeView())

    @staticmethod
    def add_extension(extension: Extension) -> None:
        Api.instance().addExtension(extension(Api.instance()))

    @classmethod
    def get_current_tool_name(cls) -> str:
        tool = cls._find_my_current_tool()
        return tool.objectName()

    @classmethod
    def _find_my_current_tool(cls):
        qwindow = Api.instance().activeWindow().qwindow()
        tool_box = cls._find_tool_box(qwindow)
        return cls._find_active_tool(tool_box)

    @staticmethod
    def _find_active_tool(qtoolbox):
        for qobj in qtoolbox.findChildren(QToolButton):
            if qobj.metaObject().className() == "KoToolBoxButton":
                if qobj.isChecked():
                    return qobj

    @staticmethod
    def _find_tool_box(qwindow):
        for qobj in qwindow.findChildren(QWidget):
            if qobj.metaObject().className() == "KoToolBox":
                return qobj


__all__ = ['Krita', 'Extension', 'QMdiArea']
