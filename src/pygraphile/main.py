import sqlite3

from utils import get_schema_from_table_name, generate_query_type, generate_type_defs

__all__ = ["PyGraphile"]


class PyGraphile:
    def __init__(self,
                 db_name: str = 'pygraphile.sqlite',
                 db_type: str = 'sqlite3',
                 migration_folder: str = 'nomigration',
                 ):

        if 'sqlite3' != db_type:
            print('this database is not supported yet')
            exit(1)

        if 'nomigration' != migration_folder:
            # TODO: apply migration
            print('need to implement this')

        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()

        result: list[tuple[str,]] = self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
        self.tables = [res[0] for res in result]
        print(f'Following tables detected {self.tables}')

        self.table_schemas = {table: get_schema_from_table_name(
            self.cursor, table) for table in self.tables}

        self.gql_type_def: str = generate_type_defs(self.table_schemas)
        self.gql_query_types: str = generate_query_type(self.table_schemas)
        print(self.gql_type_def)
        print(self.gql_query_types)


if '__main__' == __name__:
    PyGraphile()
