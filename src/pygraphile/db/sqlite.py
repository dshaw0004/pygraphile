import re
import sqlite3
from typing import Callable, Union

from ..utils import generate_query_type, generate_type_defs, sanitize_field_name

SQLITE_TO_GRAPHQL = {
    "INTEGER": "Int",
    "INT": "Int",
    "TINYINT": "Int",
    "SMALLINT": "Int",
    "MEDIUMINT": "Int",
    "BIGINT": "Int",
    "REAL": "Float",
    "FLOAT": "Float",
    "DOUBLE": "Float",
    "NUMERIC": "Float",
    "DECIMAL": "Float",
    "TEXT": "String",
    "CHAR": "String",
    "VARCHAR": "String",
    "CLOB": "String",
    "BLOB": "String",
    "BOOLEAN": "Boolean",
    "DATE": "String",
    "DATETIME": "String",
}


def get_graphql_type(col_type: Union[str, None]) -> str:
    if not col_type:
        return "String"
    base_type = re.sub(r"\(.*\)", "", str(col_type)).strip().upper()
    return SQLITE_TO_GRAPHQL.get(base_type, "String")


def get_schema_from_table_name(cursor, tablename: str) -> list[dict]:
    """PRAGMA table_info outputs cid, name, type, notnull, dflt_value, pk
    example:
    [(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0)]
    """
    safe_table = tablename.replace('"', '""')
    result: list = cursor.execute(f'PRAGMA table_info("{safe_table}")').fetchall()
    schema = [
        {
            "cid": res[0],
            "name": res[1],
            "type": get_graphql_type(res[2]),
            "notnull": res[3],
            "default": res[4],
            "primary_key": res[5],
        }
        for res in result
    ]
    return schema


class SQLiteHandler:
    tables: list[str]
    table_schemas: dict[str, list[dict[str, Union[str, int]]]]
    gql_query_types: str
    gql_type_def: str

    def __init__(self, db: str, logger: Callable[..., None]) -> None:
        logger("SQLite Handler Initialized")
        logger("Opening Datebase ", db)
        self.conn: sqlite3.Connection = sqlite3.connect(db)
        self.conn.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.conn.cursor()

        logger("Getting all tables name")
        query = (
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        result: list[tuple[str,]] = self.cursor.execute(query).fetchall()
        self.tables = [res[0] for res in result]  # list of all table names
        logger(f"Following tables detected: {self.tables}")

        self.table_schemas = {
            table: get_schema_from_table_name(self.cursor, table)
            for table in self.tables
        }

        self.gql_type_def = generate_type_defs(self.table_schemas)
        self.gql_query_types = generate_query_type(self.table_schemas)

    def make_resolver(self, table_name: str):
        if table_name not in self.tables:
            raise NameError(f"Table {table_name} not found")
        # Quote the table name to prevent SQL injection
        safe_table = table_name.replace('"', '""')

        columns = self.table_schemas.get(table_name, [])
        col_mapping = {col["name"]: sanitize_field_name(col["name"]) for col in columns}
        needs_remap = any(k != v for k, v in col_mapping.items())

        def resolver(_, info, **kwargs):
            sql = f'SELECT * FROM "{safe_table}"'
            rows = self.cursor.execute(sql).fetchall()
            if needs_remap:
                return [
                    {col_mapping.get(k, k): v for k, v in dict(row).items()}
                    for row in rows
                ]
            return [dict(row) for row in rows]

        return resolver
