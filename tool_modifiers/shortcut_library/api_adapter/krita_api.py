import os.path
from dataclasses import dataclass
from typing import Any, List


from PyQt5.QtWidgets import QWidget, QToolButton, QMainWindow
from krita import Krita as Api, Extension, QMdiArea

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.Qt import QStandardPaths

from .enums import BlendingMode, Tool


@dataclass
class Cursor:

    qwin: QMainWindow

    @property
    def x(self):
        return self.qwin.cursor().pos().x()

    @property
    def y(self):
        return self.qwin.cursor().pos().y()


@dataclass
class KritaView:

    view: Any

    def current_brush_preset_name(self) -> str:
        return self.view.currentBrushPreset().name()

    def current_blending_mode(self) -> BlendingMode:
        return BlendingMode(self.view.currentBlendingMode())

    def current_opacity(self) -> float:
        return self.view.paintingOpacity()

    def current_flow(self) -> float:
        return self.view.paintingFlow()

    def current_brush_size(self) -> float:
        return self.view.brushSize()

    def set_brush_preset(self, preset):
        self.view.setCurrentBrushPreset(preset)

    def set_blending_mode(self, mode_name: BlendingMode):
        self.view.setCurrentBlendingMode(mode_name.value)

    def set_opacity(self, opacity: float):
        self.view.setPaintingOpacity(opacity)

    def set_flow(self, flow: float):
        self.view.setPaintingFlow(flow)

    def set_brush_size(self, brush_size: float):
        self.view.setBrushSize(brush_size)


@dataclass
class Node():

    node: Any

    def name(self) -> bool:
        return self.node.name()

    def is_visible(self) -> bool:
        return self.node.visible()

    def set_visible(self, value: bool):
        return self.node.setVisible(value)

    def toggle_visible(self):
        self.set_visible(not self.is_visible())

    def is_group_layer(self) -> bool:
        return self.node.type() == "grouplayer"

    def child_nodes(self):
        return [Node(node) for node in self.node.childNodes()]

    def unique_id(self):
        return self.node.uniqueId()

    def __eq__(self, node: Any):
        if not isinstance(node, Node):
            return False
        return self.unique_id() == node.unique_id()


@dataclass
class KritaDocument:

    document: Any

    def current_node(self) -> Node:
        return Node(self.document.activeNode())

    def set_current_node(self, node: Node) -> None:
        self.document.setActiveNode(node.node)

    def top_nodes(self) -> List[Node]:
        return [Node(node) for node in self.document.topLevelNodes()]

    def all_nodes(self):
        def recursive_search(nodes: List[Node], found_so_far: List[Node]):
            for node in nodes:
                if node.is_group_layer():
                    recursive_search(node.child_nodes(), found_so_far)
                found_so_far.append(node)
            return found_so_far
        return recursive_search(self.top_nodes(), [])

    def refresh(self) -> None:
        self.document.refreshProjection()


@dataclass
class KritaCanvas:

    canvas: Any

    def rotation(self):
        return self.canvas.rotation()

    def set_rotation(self, angle_deg: float):
        self.canvas.setRotation(angle_deg)

    def zoom(self):
        return self.canvas.zoomLevel()

    def set_zoom(self, zoom: int):
        self.canvas.setZoomLevel(zoom)


class Krita:

    @staticmethod
    def get_active_view() -> KritaView:
        return KritaView(Api.instance().activeWindow().activeView())

    @classmethod
    def get_cursor(cls) -> Cursor:
        qwin = cls.get_active_qwindow()
        return Cursor(qwin)

    @staticmethod
    def get_active_document() -> KritaDocument:
        return KritaDocument(Api.instance().activeDocument())

    @staticmethod
    def get_active_canvas() -> KritaCanvas:
        return KritaCanvas(Api.instance().activeWindow().activeView().canvas())

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
        return Api.instance().resources('preset')

    @staticmethod
    def get_active_qwindow() -> QMainWindow:
        return Api.instance().activeWindow().qwindow()

    @staticmethod
    def add_extension(extension: Extension) -> None:
        Api.instance().addExtension(extension(Api.instance()))

    @classmethod
    def get_current_tool(cls) -> Tool:
        tool = cls._find_my_current_tool()
        return Tool(tool.objectName())

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


class Tag:
    def __init__(self, tag: str) -> None:
        self.name = tag
        with KritaDatabase() as database:
            preset_names = database.get_preset_names_from_tag(tag)
        self.data = sorted(set(preset_names))

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: int):
        return self.data[index]


__all__ = ['Krita', 'KritaDatabase', 'Extension', 'QMdiArea', 'Tag']
