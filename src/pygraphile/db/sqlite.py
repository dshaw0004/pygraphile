import sqlite3
from typing import Callable


SQL_TO_GRAPHQL = {
    "INTEGER": "Int",
    "TEXT": "String",
    "REAL": "Float",
    "BLOB": "String",  # or custom scalar
}


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


def generate_type_defs(tables):
    type_defs = []
    for table_name, columns in tables.items():
        fields = []
        for col in columns:
            gql_type = SQL_TO_GRAPHQL.get((col["type"] or "").upper(), "String")
            not_null = "!" if col["notnull"] else ""
            fields.append(f"{col['name']}: {gql_type}{not_null}")
        type_def = f"type {table_name.capitalize()} {{\n  " + \
            "\n  ".join(fields) + "\n}"
        type_defs.append(type_def)
    return "\n".join(type_defs)


def generate_query_type(tables):
    queries = []
    for table_name in tables.keys():
        gql_name = table_name.capitalize()
        queries.append(f"{table_name}: [{gql_name}]")
    return "type Query {\n  " + "\n  ".join(queries) + "\n}"


class SQLiteHandler:
    tables: list[str]
    table_schemas: dict[str, list[dict[str, str | int]]]
    gql_query_types: str
    gql_type_def: str

    def __init__(self, db: str, logger: Callable[..., None]) -> None:
        logger('SQLite Handler Initialized')
        logger('Opening Datebase ', db)
        self.conn: sqlite3.Connection = sqlite3.connect(db)
        self.conn.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.conn.cursor()

        logger('Getting all tables name')
        result: list[tuple[str,]] = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
        self.tables = [res[0] for res in result] # list of all table names
        logger(f'Following tables detected: {self.tables}')

        self.table_schemas = {
            table: get_schema_from_table_name(self.cursor, table)
            for table in self.tables
        }

        self.gql_type_def = generate_type_defs(self.table_schemas)
        self.gql_query_types = generate_query_type(self.table_schemas)

    def make_resolver(self, table_name: str):
        # Quote the table name to prevent SQL injection
        safe_table = table_name.replace('"', '""')
        if safe_table not in self.tables:
            raise NameError(f'Table {table_name} not found')

        def resolver(_, info, **kwargs):
            sql = f'SELECT * FROM "{safe_table}"'
            rows = self.cursor.execute(sql).fetchall()
            return [dict(row) for row in rows]

        return resolver
