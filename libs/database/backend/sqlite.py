'''SQLLite System'''
import sqlite3
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.database.backend.base import BackendBase
from libs.database.table import Table
from libs.database.backend.db.table_version import TABLE_VERSION_DB_INFO
#https://docs.python.org/3/library/sqlite3.html
def dict_factory(cursor, row):
    '''makes the return data from the database a dict'''
    return_data = {}
    for idx, col in enumerate(cursor.description):
        return_data[col[0]] = row[idx]
    return return_data

class SQLite(BackendBase):
    '''SQLite system'''

    def __startup(self):
        '''Setup SQLlite Here'''
        super().__conn = sqlite3.connect(PROGRAMCONFIGLOCATION + '/Tackem.db')
        super().__conn.row_factory = dict_factory
        if not self.__check_version_table_exists():
            self.__add_table(TABLE_VERSION_DB_INFO, False)

    def __shutdown(self):
        '''Shutdown the System Here'''
        # save any changes to the file
        super().__conn.commit()
        # close the connection
        super().__conn.close()

    def __get_cursor(self):
        '''returns a sql cursor'''
        return super().__conn.cursor()

    def __table_check(self, table: Table) -> bool:
        '''checks if the table exists adds it if it doesn't and update it if needed'''
        table_version = self.__table_exists(table.name)
        if table_version == table.version:
            return True
        if table_version == 0:
            return self.__add_table(table)
        if table_version < table.version:
            return self.__update_table(table)
        return False

    def __get(self, call: str) -> list:
        '''Grab a list of the tables'''
        cursor = super().__conn.execute(call)
        return cursor.fetchall()

    def __check_version_table_exists(self) -> bool:
        '''checks if the table_version exists'''
        cursor = super().__conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='table_version';"
        )
        return bool(cursor.rowcount())

    def __table_exists(self, table_name: str) -> int:
        '''Check if Table Exists return version number'''
        cursor = super().__conn.execute(
            "SELECT version FROM table_version WHERE name=?;",
            (table_name,)
        )

        if info := cursor.fetchone():
            return info['version']
        return 0

    def __add_table(self, table: Table, update_version_table: bool = True) -> bool:
        ''' Adds Table to the DB and then adds it into the table version DB'''
        cursor = super().__conn.execute(
            f"CREATE TABLE IF NOT EXISTS ? ({', '.join(['?' for _ in range(len(table.data))])});",
            (
                table.name,
                *table.columns,
            )
        )
        cursor.commit()
        if update_version_table:
            super().__conn.execute(
                "INSERT INTO table_version (name, version) VALUES (?, ?);",
                (table.name, table.version)
            )
            super().__conn.commit()
        return True

    def __update_table(self, table: Table) -> bool:
        '''Update the table with the informaiton provided'''

        # first move the current table to a new name
        super().__conn.execute(
            "ALTER TABLE ? RENAME TO ?;",
            (table.name, f"{table.name}_old")
        )
        super().__conn.commit()

        # make the new version of the table
        self.__add_table(table, False)

        cursor = super().__conn.execute(
            "SELECT * FROM ?;",
            (f"{table.name}_old", )
        )
        old_dict = cursor.fetchall()

        if old_dict:
            keys = old_dict.keys()
            items = [(* single_dict.items(), ) for single_dict in old_dict]
            qmarks = ["'?'"] * len(keys)
            super().__conn.executemany(
                f"INSERT INTO {table.name} ({', '.join(keys)}) Values ({', '.join(qmarks)})",
                (
                    items,
                )
            )

        super().__conn.commit()

        # delete old table
        super().__conn.execute("DROP TABLE ?;", (f"{table.name}_old", ))
        super().__conn.commit()

        return True
