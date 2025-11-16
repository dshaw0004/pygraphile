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


SQL_TO_GRAPHQL = {
    "INTEGER": "Int",
    "TEXT": "String",
    "REAL": "Float",
    "BLOB": "String",  # or custom scalar
}


def generate_type_defs(tables):
    type_defs = []
    for table_name, columns in tables.items():
        fields = []
        for col in columns:
            gql_type = SQL_TO_GRAPHQL.get(col["type"].upper(), "String")
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

