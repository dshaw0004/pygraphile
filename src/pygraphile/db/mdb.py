import re
from typing import Union, Callable
from urllib.parse import urlparse, unquote
import mariadb

SQL_TO_GRAPHQL = {
    # Integer types
    'TINYINT': 'Int',
    'SMALLINT': 'Int',
    'MEDIUMINT': 'Int',
    'INT': 'Int',
    'INTEGER': 'Int',
    'BIGINT': 'Int',  # or custom 'BigInt' scalar
    'YEAR': 'Int',

    # Boolean-ish
    'BOOLEAN': 'Boolean',
    'BOOL': 'Boolean',

    # Floating point / decimal
    'FLOAT': 'Float',
    'DOUBLE': 'Float',
    'DECIMAL': 'Float',  # or custom 'Decimal' scalar
    'NUMERIC': 'Float',

    # String types
    'CHAR': 'String',
    'VARCHAR': 'String',
    'TEXT': 'String',
    'TINYTEXT': 'String',
    'MEDIUMTEXT': 'String',
    'LONGTEXT': 'String',
    'ENUM': 'String',
    'SET': 'String',

    # Date/time
    'DATE': 'String',       # or custom 'Date' scalar
    'DATETIME': 'String',   # or custom 'DateTime' scalar
    'TIMESTAMP': 'String',  # or custom 'DateTime' scalar
    'TIME': 'String',       # or custom 'Time' scalar

    # Binary
    'BLOB': 'String',       # or custom scalar
    'TINYBLOB': 'String',
    'MEDIUMBLOB': 'String',
    'LONGBLOB': 'String',
    'BINARY': 'String',
    'VARBINARY': 'String',

    # Other
    'JSON': 'JSON',  # custom scalar
    'BIT': 'Boolean',
}

def get_graphql_type(col_type: str) -> str:
    base_type = re.sub(r'\(.*\)', '', col_type).strip().upper()
    if col_type.lower().startswith('tinyint(1)'):
        return 'Boolean'  # handle bool-as-tinyint(1) before generic lookup
    return SQL_TO_GRAPHQL.get(base_type, 'String')

def get_db_config_from_uri(db: str):
    """Convert mysql://user:pass@host:port/dbname into a db_config dict."""
    parsed = urlparse(db)
    return {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 3306,
        'user': unquote(parsed.username) if parsed.username else None,
        'password': unquote(parsed.password) if parsed.password else None,
        'database': parsed.path.lstrip('/') or None,
    }

def get_table_schema(table_name: str, cursor: mariadb.Cursor):
    '''Get schema of a table.
    '''
    cursor.execute(f'DESCRIBE `{table_name}`')
    schema = []
    for column in cursor.fetchall():
        schema.append({
            'name': column.get('Field'),
            'type': get_graphql_type(column.get('Type')),
            'notnull' : 0 if column.get('Null', 'No') == 'No' else 1,
            'default' : column.get('Default', None),
            'primary_key' : 1 if column.get('Key', '') == 'PRI' else 0,
        })
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



class MariaDBHandler:
    tables: list[str]
    table_schemas: dict[str, list[dict[str, Union[str, int]]]]
    gql_query_types: str
    gql_type_def: str

    def __init__(self, db: str, logger: Callable[..., None]) -> None:
        self.db = db
        self._log = logger
        logger('MariaDB Handler Initialized')
        logger('Opening database ', db)
        db_config = get_db_config_from_uri(db)
        self.conn: mariadb.Connection = mariadb.connect(**db_config)
        self.cursor: mariadb.Cursor = self.conn.cursor(dictionary=True)

        self.cursor.execute("SHOW TABLES;")
        show_tables = [row for row in self.cursor]

        self.tables = [row.get(f'Tables_in_{db_config["database"]}') for row in show_tables]

        self.table_schemas = {
            table: get_table_schema(table, self.cursor) 
            for table in self.tables
        }

        self.gql_type_def = generate_type_defs(self.table_schemas)
        self.gql_query_types = generate_query_type(self.table_schemas)



    def make_resolver(self, table_name: str) -> Callable[..., Callable[..., list[dict]]]:
        # Quote the table name to prevent SQL injection
        safe_table = table_name.replace('"', '""')
        if safe_table not in self.tables:
            raise NameError(f'Table {table_name} not found')

        def resolver(_, info, **kwargs):
            sql = f'SELECT * FROM `{safe_table}`'
            self.cursor.execute(sql)
            return [dict(row) for row in self.cursor]

        return resolver

# if __name__ == "__main__":
#     mdb = MariaDBHandler('mariadb://root:password@127.0.0.1:3306/_7888266aa49ff9a5', print)
    # a = mdb.make_resolver('tabUser')
    # print(a(1, 2))
