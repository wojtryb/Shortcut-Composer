# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import os.path
from typing import Any

from krita import Krita as Api
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class Database:
    """Explorer of the database with krita resources."""

    connection_name = "ShortcutComposer"

    def __init__(self) -> None:
        self.connect_if_needed()

    @classmethod
    def connect_if_needed(cls) -> None:
        """Connect to krita database if it was not done already."""
        if cls.connection_name in QSqlDatabase.connectionNames():
            return

        cls.database = QSqlDatabase.addDatabase("QSQLITE", cls.connection_name)
        path = Api.instance().readSetting("", "ResourceDirectory", "")
        path = os.path.join(path, "resourcecache.sqlite")
        cls.database.setDatabaseName(path)

    def _single_column_query(self, sql_query: str, value: str) -> list[Any]:
        """Use SQL query to get single column in a form of a list."""
        if not self.database.open():
            return []

        query_handler = QSqlQuery(self.database)
        if not query_handler.exec(sql_query):
            return []

        return_list = []
        while query_handler.next():
            return_list.append(query_handler.value(value))

        query_handler.finish()
        return return_list

    def get_preset_names_from_tag(self, tag_name: str) -> list[str]:
        """Return list of all preset names that belong to given tag."""
        tag_name = tag_name.replace("\"", "\"\"")
        sql_query = f'''
            SELECT DISTINCT r.name AS preset
            FROM tags t
                JOIN resource_tags rt
                    ON t.id=rt.tag_id
                JOIN resources r
                    ON r.id = rt.resource_id
            WHERE
                t.name="{tag_name}"
                AND rt.active = 1
        '''
        return self._single_column_query(sql_query, "preset")

    def get_brush_tags(self) -> list[str]:
        "Return list of all tag names."
        sql_query = '''
            SELECT DISTINCT t.name AS tag
            FROM tags t
            WHERE
                t.active = 1
                AND t.resource_type_id = 5
        '''
        presets = self._single_column_query(sql_query, "tag")
        return sorted(presets, key=str.lower)

    def close(self) -> None:
        """Close the connection with the database."""
        self.database.close()

    def __enter__(self) -> 'Database':
        """Return self. Connection already initialized in init."""
        return self

    def __exit__(self, *_) -> None:
        """Close the connection with the database on exit."""
        self.close()
