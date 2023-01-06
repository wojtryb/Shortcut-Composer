import os.path
from typing import List

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.Qt import QStandardPaths


class Database:
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

    def close(self) -> None:
        self.database.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
