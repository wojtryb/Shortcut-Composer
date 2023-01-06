import os.path
from typing import List

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.Qt import QStandardPaths


class Database:
    """Explorer of the database with krita resources."""

    def __init__(self):
        """Connect to the database with krita resources."""
        database_path = os.path.join(
            QStandardPaths.standardLocations(QStandardPaths.DataLocation)[0],
            'resourcecache.sqlite'
        )
        self.database = QSqlDatabase.addDatabase("QSQLITE", "dbResources")
        self.database.setDatabaseName(database_path)

    def single_value_query(self, sql_query: str, value: str) -> List[str]:
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

    def get_preset_names_from_tag(self, tag_name: str) -> List[str]:
        """Return list of all preset names that belong to passed tag."""
        sql_query = f'''
            SELECT r.name AS preset
            FROM tags t
                JOIN resource_tags rt
                    ON t.id=rt.tag_id
                JOIN resources r
                    ON r.id = rt.resource_id
            WHERE t.name='{tag_name}'
        '''
        return self.single_value_query(sql_query, "preset")

    def get_brush_tags(self) -> List[str]:
        sql_query = '''
            SELECT t.name AS tag
            FROM tags t
        '''
        return self.single_value_query(sql_query, "tag")

    def close(self) -> None:
        """Close the connection with the database."""
        self.database.close()

    def __enter__(self):
        """Return self. Connection already initialized in init."""
        return self

    def __exit__(self, *_):
        """Close the connection with the database on exit."""
        self.close()


"★ My Favorites"
