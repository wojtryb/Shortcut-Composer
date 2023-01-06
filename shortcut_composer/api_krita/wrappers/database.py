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

    def get_preset_names_from_tag(self, tag_name: str) -> List[str]:
        """Return list of all preset names that belong to passed tag."""
        if not self.database.open():
            return []

        sql_query = f'''
            SELECT r.name AS preset
            FROM tags t
                JOIN resource_tags rt
                    ON t.id=rt.tag_id
                JOIN resources r
                    ON r.id = rt.resource_id
            WHERE t.name='{tag_name}'
        '''
        query_handler = QSqlQuery(self.database)
        if not query_handler.exec(sql_query):
            return []

        preset_names = []
        while query_handler.next():
            preset_names.append(query_handler.value('preset'))

        query_handler.finish()
        return preset_names

    def close(self) -> None:
        """Close the connection with the database."""
        self.database.close()

    def __enter__(self):
        """Return self. Connection already initialized in init."""
        return self

    def __exit__(self, *_):
        """Close the connection with the database on exit."""
        self.close()
