import os.path
from dataclasses import dataclass
from typing import Any, List

from PyQt5.QtWidgets import QWidget, QToolButton, QMainWindow
from krita import Krita as Api, Extension, QMdiArea

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.Qt import QStandardPaths


@dataclass
class KritaView:

    view: Any

    def current_brush_preset_name(self) -> str:
        return self.view.currentBrushPreset().name()

    def current_blending_mode(self):
        return self.view.currentBlendingMode()

    def current_opacity(self) -> int:
        return self.view.paintingOpacity()

    def set_brush_preset(self, preset):
        self.view.setCurrentBrushPreset(preset)

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
    def get_presets() -> dict:
        # print(Api.instance().resources('preset'))
        return Api.instance().resources('preset')

    @staticmethod
    def get_active_view() -> KritaView:
        return KritaView(Api.instance().activeWindow().activeView())

    def get_active_qwindow() -> QMainWindow:
        return Api.instance().activeWindow().qwindow()

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


class KritaDatabase:
    def __init__(self):
        database_path = os.path.join(
            QStandardPaths.standardLocations(QStandardPaths.DataLocation)[0],
            'resourcecache.sqlite')

        self.database = QSqlDatabase.addDatabase("QSQLITE", "dbResources")
        self.database.setDatabaseName(database_path)

    # def get_presets_from_tag(self, tag):
    #     all_preset_objects = Krita.get_presets()
    #     preset_names = self.get_preset_names_from_tag(tag)

    #     return [preset_names[preset] for preset in all_preset_objects]

    def get_preset_names_from_tag(self, tag) -> List[str]:
        if not self.database.open():
            return []

        sql_query = f'''
            SELECT r.name AS preset
            from tags t
                    join resource_tags rt
                    on t.id=rt.tag_id
                    join resources r
                    on r.id = rt.resource_id
            where t.name='{tag}'
        '''
        query_handler = QSqlQuery(self.database)
        if not query_handler.exec(sql_query):
            return []

        preset_names = []
        while query_handler.next():
            preset_names.append(query_handler.value('preset'))

        query_handler.finish()
        return preset_names

    def close(self):
        self.database.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


__all__ = ['Krita', 'KritaDatabase', 'Extension', 'QMdiArea']
