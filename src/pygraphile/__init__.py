import sqlite3
"""
PyGraphile - A Python library for automatically generating GraphQL APIs from databases.

Inspired by PostGraphile, this library introspects your database schema and
creates a GraphQL API with queries, mutations, and subscriptions.

Currently supports SQLite with plans for PostgreSQL, MySQL, and other databases.
"""
from .main import PyGraphile
from .utils import get_schema_from_table_name, generate_query_type, generate_type_defs, SQL_TO_GRAPHQL

__version__ = "0.1.0"
__author__ = "dshaw0004"
__all__ = ["__version__", "PyGraphile", "get_schema_from_table_name", "generate_type_defs", "generate_query_type", "SQL_TO_GRAPHQL"]


