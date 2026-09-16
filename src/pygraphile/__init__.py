"""
PyGraphile - A Python library for automatically generating GraphQL APIs from databases.

Inspired by PostGraphile, this library introspects your database schema and
creates a GraphQL API with queries, mutations, and subscriptions.

Currently supports SQLite, MariaDB, and MySQL, with PostgreSQL on the roadmap.
"""

from .main import PyGraphile
from .utils import (
    SQL_TO_GRAPHQL,
    generate_query_type,
    generate_type_defs,
    get_schema_from_table_name,
    sanitize_field_name,
    sanitize_type_name,
)

__version__ = "0.6.2"
__author__ = "dshaw0004"
__all__ = [
    "__version__",
    "PyGraphile",
    "get_schema_from_table_name",
    "generate_type_defs",
    "generate_query_type",
    "sanitize_field_name",
    "sanitize_type_name",
    "SQL_TO_GRAPHQL",
]
