import re
from typing import Any, Union

SQL_TO_GRAPHQL = {
    "INTEGER": "Int",
    "TEXT": "String",
    "REAL": "Float",
    "BLOB": "String",
}


def get_schema_from_table_name(cursor, tablename: str) -> list[dict]:
    """
    PRAGMA table_info outputs cid, name, type, notnull, dflt_value, pk
    example:
    [(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0)]
    """
    safe_table = tablename.replace('"', '""')
    result: list = cursor.execute(f'PRAGMA table_info("{safe_table}")').fetchall()
    schema = [
        {
            "cid": res[0],
            "name": res[1],
            "type": res[2],
            "notnull": res[3],
            "default": res[4],
            "primary_key": res[5],
        }
        for res in result
    ]
    return schema


def sanitize_field_name(name: str) -> str:
    """Sanitize a database table or column name into a valid GraphQL field name.

    GraphQL name format: /[_A-Za-z][_0-9A-Za-z]*/
    """
    if not name:
        return "unnamed"
    # Replace spaces and any character that is not alphanumeric or underscore with '_'
    sanitized = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip())
    # Avoid reserved GraphQL introspection prefix '__'
    sanitized = re.sub(r"^_+", "_", sanitized)
    # GraphQL names cannot start with a digit
    if sanitized and sanitized[0].isdigit():
        sanitized = f"_{sanitized}"
    if not sanitized or sanitized == "_":
        return "unnamed"
    return sanitized


def sanitize_type_name(name: str) -> str:
    """Sanitize a database table name into a valid GraphQL type name (PascalCase).

    GraphQL name format: /[_A-Za-z][_0-9A-Za-z]*/
    """
    if not name:
        return "Unnamed"
    # Split by non-alphanumeric characters
    words = [w for w in re.split(r"[^a-zA-Z0-9]+", name.strip()) if w]
    if not words:
        return "Unnamed"
    # Capitalize the first letter of each word to form PascalCase
    # while preserving inner case
    type_name = "".join(word[0].upper() + word[1:] for word in words)
    # GraphQL names cannot start with a digit
    if type_name and type_name[0].isdigit():
        type_name = f"_{type_name}"
    # Avoid collision with root GraphQL operation type names
    if type_name in ("Query", "Mutation", "Subscription"):
        type_name = f"{type_name}Table"
    return type_name


def generate_type_defs(tables: dict[str, list[dict[str, Any]]]) -> str:
    type_defs = []
    for table_name, columns in tables.items():
        type_name = sanitize_type_name(table_name)
        fields = []
        for col in columns:
            col_name = sanitize_field_name(col["name"])
            gql_type = col.get("type") or "String"
            not_null = "!" if col.get("notnull") else ""
            fields.append(f"{col_name}: {gql_type}{not_null}")
        type_def = f"type {type_name} {{\n  " + "\n  ".join(fields) + "\n}"
        type_defs.append(type_def)
    return "\n".join(type_defs)


def generate_query_type(tables: Union[dict, list]) -> str:
    queries = []
    table_keys = tables.keys() if isinstance(tables, dict) else tables
    for table_name in table_keys:
        gql_type_name = sanitize_type_name(table_name)
        gql_field_name = sanitize_field_name(table_name)
        queries.append(f"{gql_field_name}: [{gql_type_name}]")
    return "type Query {\n  " + "\n  ".join(queries) + "\n}"
