import sqlite3
import tempfile

from ariadne import graphql_sync

from pygraphile import (
    PyGraphile,
    generate_query_type,
    generate_type_defs,
    sanitize_field_name,
    sanitize_type_name,
)


def test_sanitize_field_name():
    assert sanitize_field_name("users") == "users"
    assert sanitize_field_name("tabapi request log") == "tabapi_request_log"
    assert sanitize_field_name("first name") == "first_name"
    assert sanitize_field_name("order-items") == "order_items"
    assert sanitize_field_name("2024_sales") == "_2024_sales"
    assert sanitize_field_name("__secret") == "_secret"
    assert sanitize_field_name("") == "unnamed"


def test_sanitize_type_name():
    assert sanitize_type_name("users") == "Users"
    assert sanitize_type_name("tabapi request log") == "TabapiRequestLog"
    assert sanitize_type_name("tabUser") == "TabUser"
    assert sanitize_type_name("order_items") == "OrderItems"
    assert sanitize_type_name("order-items") == "OrderItems"
    assert sanitize_type_name("2024_reports") == "_2024Reports"
    assert sanitize_type_name("Query") == "QueryTable"
    assert sanitize_type_name("") == "Unnamed"


def test_generate_type_defs_and_query():
    tables = {
        "tabapi request log": [
            {"name": "name", "type": "String", "notnull": 1},
            {"name": "request data", "type": "String", "notnull": 0},
        ]
    }
    type_defs = generate_type_defs(tables)
    assert "type TabapiRequestLog {" in type_defs
    assert "name: String!" in type_defs
    assert "request_data: String" in type_defs

    query_type = generate_query_type(tables)
    assert "tabapi_request_log: [TabapiRequestLog]" in query_type


def test_sqlite_with_spaces_in_table_and_column_names():
    with tempfile.NamedTemporaryFile(suffix=".sqlite") as tmp:
        conn = sqlite3.connect(tmp.name)
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE "tabapi request log" '
            '("id" INTEGER PRIMARY KEY, "full name" TEXT);'
        )
        cursor.execute(
            'INSERT INTO "tabapi request log" ("id", "full name") VALUES (1, "Alice");'
        )
        conn.commit()
        conn.close()

        pg = PyGraphile(tmp.name, db_type="sqlite", debug=True)
        assert pg.schema is not None

        # Execute a GraphQL query against the sanitized names
        query_str = "{ tabapi_request_log { id full_name } }"
        success, result = graphql_sync(pg.schema, {"query": query_str})
        assert success
        assert result["data"] == {
            "tabapi_request_log": [{"id": 1, "full_name": "Alice"}]
        }
