import re
from typing import Callable, Union
from urllib.parse import unquote, urlparse

import mariadb

from ..utils import generate_query_type, generate_type_defs, sanitize_field_name

SQL_TO_GRAPHQL = {
    # Integer types
    "TINYINT": "Int",
    "SMALLINT": "Int",
    "MEDIUMINT": "Int",
    "INT": "Int",
    "INTEGER": "Int",
    "BIGINT": "Int",  # or custom 'BigInt' scalar
    "YEAR": "Int",
    # Boolean-ish
    "BOOLEAN": "Boolean",
    "BOOL": "Boolean",
    # Floating point / decimal
    "FLOAT": "Float",
    "DOUBLE": "Float",
    "DECIMAL": "Float",  # or custom 'Decimal' scalar
    "NUMERIC": "Float",
    # String types
    "CHAR": "String",
    "VARCHAR": "String",
    "TEXT": "String",
    "TINYTEXT": "String",
    "MEDIUMTEXT": "String",
    "LONGTEXT": "String",
    "ENUM": "String",
    "SET": "String",
    # Date/time
    "DATE": "String",  # or custom 'Date' scalar
    "DATETIME": "String",  # or custom 'DateTime' scalar
    "TIMESTAMP": "String",  # or custom 'DateTime' scalar
    "TIME": "String",  # or custom 'Time' scalar
    # Binary
    "BLOB": "String",  # or custom scalar
    "TINYBLOB": "String",
    "MEDIUMBLOB": "String",
    "LONGBLOB": "String",
    "BINARY": "String",
    "VARBINARY": "String",
    # Other
    "JSON": "String",
    "BIT": "Boolean",
}


def get_graphql_type(col_type: str) -> str:
    base_type = re.sub(r"\(.*\)", "", col_type).strip().upper()
    if col_type.lower().startswith("tinyint(1)"):
        return "Boolean"  # handle bool-as-tinyint(1) before generic lookup
    return SQL_TO_GRAPHQL.get(base_type, "String")


def get_db_config_from_uri(db: str):
    """Convert mysql://user:pass@host:port/dbname into a db_config dict."""
    parsed = urlparse(db)
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 3306,
        "user": unquote(parsed.username) if parsed.username else None,
        "password": unquote(parsed.password) if parsed.password else None,
        "database": parsed.path.lstrip("/") or None,
    }


def get_table_schema(table_name: str, cursor: mariadb.Cursor):
    """Get schema of a table."""
    cursor.execute(f"DESCRIBE `{table_name}`")
    schema = []
    for column in cursor.fetchall():
        schema.append(
            {
                "name": column.get("Field"),
                "type": get_graphql_type(column.get("Type")),
                "notnull": 0 if column.get("Null", "No") == "No" else 1,
                "default": column.get("Default", None),
                "primary_key": 1 if column.get("Key", "") == "PRI" else 0,
            }
        )
    return schema


class MariaDBHandler:
    tables: list[str]
    table_schemas: dict[str, list[dict[str, Union[str, int]]]]
    gql_query_types: str
    gql_type_def: str

    def __init__(self, db: str, logger: Callable[..., None]) -> None:
        self.db = db
        self._log = logger
        logger("MariaDB Handler Initialized")
        logger("Opening database ", db)
        db_config = get_db_config_from_uri(db)
        self.conn: mariadb.Connection = mariadb.connect(**db_config)
        self.cursor: mariadb.Cursor = self.conn.cursor(dictionary=True)

        self.cursor.execute("SHOW TABLES;")
        show_tables = [row for row in self.cursor]

        self.tables = [
            row.get(f"Tables_in_{db_config['database']}") for row in show_tables
        ]

        self.table_schemas = {
            table: get_table_schema(table, self.cursor) for table in self.tables
        }

        self.gql_type_def = generate_type_defs(self.table_schemas)
        self.gql_query_types = generate_query_type(self.table_schemas)

    def make_resolver(self, table_name: str) -> Callable[..., list[dict]]:
        if table_name not in self.tables:
            raise NameError(f"Table {table_name} not found")
        # Quote the table name to prevent SQL injection and support special characters
        safe_table = table_name.replace("`", "``")

        columns = self.table_schemas.get(table_name, [])
        col_mapping = {col["name"]: sanitize_field_name(col["name"]) for col in columns}
        needs_remap = any(k != v for k, v in col_mapping.items())

        def resolver(_, info, **kwargs):
            sql = f"SELECT * FROM `{safe_table}`"
            self.cursor.execute(sql)
            if needs_remap:
                return [
                    {col_mapping.get(k, k): v for k, v in dict(row).items()}
                    for row in self.cursor
                ]
            return [dict(row) for row in self.cursor]

        return resolver
