from typing import TYPE_CHECKING, Union

from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.explorer import ExplorerApollo

from .db.sqlite import SQLiteHandler
from .utils import sanitize_field_name

if TYPE_CHECKING:
    from .db.mdb import MariaDBHandler

__all__ = ["PyGraphile"]
SUPPORTED_DATABASES = "sqlite3", "sqlite", "mariadb", "mysql"


class PyGraphile:
    handler: Union[SQLiteHandler, "MariaDBHandler", None] = None
    _debug: bool = False

    def log(self, *args):
        if self._debug:
            print(*args)

    def is_supported(self, db_type: str) -> bool:
        if db_type not in SUPPORTED_DATABASES:
            raise ValueError(
                f"Unsupported database type: '{db_type}'. "
                f"Currently only {SUPPORTED_DATABASES} are supported."
            )
        if db_type in ("mariadb", "mysql"):
            try:
                import mariadb  # noqa: F401

                return True
            except ImportError as e:
                raise ImportError(
                    f"{db_type} support requires extra dependency. "
                    f"Install with: 'pygraphile[{db_type}]'"
                ) from e
        return True

    def __init__(
        self,
        db_name: str = "pygraphile.sqlite",
        db_type: str = "sqlite",
        migration_folder: str = "nomigration",
        debug: bool = False,
    ):
        self._debug = debug
        self.is_supported(db_type=db_type)

        if db_type in ("sqlite", "sqlite3"):
            self.handler = SQLiteHandler(db=db_name, logger=self.log)
        elif db_type in ("mariadb", "mysql"):
            from .db.mdb import MariaDBHandler

            self.handler = MariaDBHandler(db=db_name, logger=self.log)

        if migration_folder != "nomigration":
            # TODO: apply migration
            print("need to implement this")

        self.tables = self.handler.tables

        self.table_schemas = self.handler.table_schemas

        self.gql_type_def: str = self.handler.gql_type_def
        self.gql_query_types: str = self.handler.gql_query_types

        query = QueryType()

        # dynamically attach resolvers
        for table in self.tables:
            query.set_field(
                sanitize_field_name(table), self.handler.make_resolver(table)
            )

        type_defs = self.gql_type_def + "\n" + self.gql_query_types
        self.schema = make_executable_schema(type_defs, query)

    def get_query_app(self):
        return GraphQL(
            self.schema,
            debug=self._debug,
            explorer=ExplorerApollo() if self._debug else None,
        )
