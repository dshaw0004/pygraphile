from typing import Union
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.explorer import ExplorerApollo

from .db.sqlite import SQLiteHandler

__all__ = ["PyGraphile"]
SUPPORTED_DATABASES = 'sqlite3', 'sqlite'


class PyGraphile:
    handler: Union[SQLiteHandler, None] = None
    _debug: bool = False

    def log(self, *args):
        if self._debug:
            print(*args)

    def __init__(
        self,
        db_name: str = 'pygraphile.sqlite',
        db_type: str = 'sqlite',
        migration_folder: str = 'nomigration',
        debug: bool = False,
    ):
        self._debug = debug
        if db_type not in SUPPORTED_DATABASES:
            raise ValueError(f"Unsupported database type: '{db_type}'. Currently only {SUPPORTED_DATABASES} are supported.")

        if db_type == 'sqlite':
            self.handler = SQLiteHandler(db=db_name, logger=self.log)

        if migration_folder != 'nomigration':
            # TODO: apply migration
            print('need to implement this')

        self.tables = self.handler.tables

        self.table_schemas = self.handler.table_schemas

        self.gql_type_def: str = self.handler.gql_type_def
        self.gql_query_types: str = self.handler.gql_query_types

        query = QueryType()

        # dynamically attach resolvers
        for table in self.tables:
            query.set_field(table, self.handler.make_resolver(table))

        type_defs = self.gql_type_def + "\n" + self.gql_query_types
        self.schema = make_executable_schema(type_defs, query)

    def get_query_app(self):
        return GraphQL(self.schema, debug=self._debug, explorer=ExplorerApollo() if self._debug else None)

