import sqlite3
"""
PyGraphile - A Python library for automatically generating GraphQL APIs from databases.

Inspired by PostGraphile, this library introspects your database schema and
creates a GraphQL API with queries, mutations, and subscriptions.

Currently supports SQLite with plans for PostgreSQL, MySQL, and other databases.
"""

__version__ = "0.1.0"
__author__ = "dshaw0004"
__all__ = ["__version__", "PyGraphile"]


def get_schema_from_table_name(cursor, tablename: str) -> list[dict]:
    '''
    PRAGMA table_info outputs cid, name, type, notnull, dflt_value, pk
    example:
    [(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0)]
    '''
    result: list = cursor.execute(f"PRAGMA table_info({tablename})").fetchall()
    schema = [{
        'cid': res[0],
        'name': res[1],
        'type': res[2],
        'notnull': res[3],
        'default': res[4],
        'primary_key': res[5],
    } for res in result]
    return schema


class PyGraphile:
    def __init__(self,
                 db_name: str = 'pygraphile.sqlite',
                 db_type: str = 'sqlite3',
                 migration_folder: str = 'nomigration',
                 ):

        if 'sqlite3' != db_type:
            print('this database is not supported yet')
            exit(1)

        if 'nomigration' != migration_folder:
            # TODO: apply migration
            print('need to implement this')

        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()

        result: list[tuple[str,]] = self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
        self.tables = [res[0] for res in result]
        print(f'Following tables detected {self.tables}')

        self.table_schemas = get_schema_from_table_name(self.cursor, self.tables[0])

