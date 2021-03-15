"""SQLLite System"""
import sqlite3

from data import PROGRAMCONFIGLOCATION
from data.database.system import TABLE_VERSION_DB
from libs.database.backend.base import BackendBase
from libs.database.table import Table

# https://docs.python.org/3/library/sqlite3.html


def dict_factory(cursor, row):
    """makes the return data from the database a dict"""
    return_data = {}
    for idx, col in enumerate(cursor.description):
        return_data[col[0]] = row[idx]
    return return_data


class SQLite(BackendBase):
    """SQLite system"""

    def _startup(self):
        """Setup SQLlite Here"""
        BackendBase._conn = sqlite3.connect(PROGRAMCONFIGLOCATION + "/Tackem.db")
        BackendBase._conn.row_factory = dict_factory
        if not self.__check_version_table_exists():
            self.__add_table(TABLE_VERSION_DB, False)

    def _shutdown(self):
        """Shutdown the System Here"""
        # save any changes to the file
        BackendBase._conn.commit()
        # close the connection
        BackendBase._conn.close()

    def _get_cursor(self):
        """returns a sql cursor"""
        return BackendBase._conn.cursor()

    def _table_check(self, table: Table) -> bool:
        """checks if the table exists adds it if it doesn't and update it if needed"""
        table_version = self.__table_exists(table.name())
        if table_version == table.version:
            return True
        if table_version == 0:
            return self.__add_table(table)
        if table_version < table.version:
            return self.__update_table(table)
        return False

    def __get(self, call: str) -> list:
        """Grab a list of the tables"""
        cursor = BackendBase._conn.execute(call)
        return cursor.fetchall()

    def __check_version_table_exists(self) -> bool:
        """checks if the table_version exists"""
        cursor = BackendBase._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='table_version';"
        )
        return bool(cursor.rowcount > 0)

    def __table_exists(self, table_name: str) -> int:
        """Check if Table Exists return version number"""
        cursor = BackendBase._conn.execute(
            "SELECT version FROM table_version WHERE name=?;", (table_name,)
        )

        if info := cursor.fetchone():
            return info["version"]
        return 0

    def __add_table(self, table: Table, update_version_table: bool = True) -> bool:
        """ Adds Table to the DB and then adds it into the table version DB"""
        query = f"CREATE TABLE IF NOT EXISTS {table.name()}({', '.join(table.columns)});"
        BackendBase._conn.execute(query)
        BackendBase._conn.commit()
        if update_version_table:
            BackendBase._conn.execute(
                "INSERT INTO table_version (name, version) VALUES (?, ?);",
                (table.name(), table.version),
            )
            BackendBase._conn.commit()
        return True

    def __update_table(self, table: Table) -> bool:
        """Update the table with the informaiton provided"""

        # first move the current table to a new name
        BackendBase._conn.execute(f"ALTER TABLE {table.name()} RENAME TO {table.name()}_old;")
        BackendBase._conn.commit()

        # make the new version of the table
        self.__add_table(table, False)

        cursor = BackendBase._conn.execute(f"SELECT * FROM {table.name()}_old;")
        old_dict = cursor.fetchall()

        if old_dict:
            keys = old_dict.keys()
            items = [(*single_dict.items(),) for single_dict in old_dict]
            qmarks = ["'?'"] * len(keys)
            BackendBase._conn.executemany(
                f"INSERT INTO {table.name()} ({', '.join(keys)}) Values ({', '.join(qmarks)})",
                (items,),
            )

        BackendBase._conn.commit()

        # delete old table
        BackendBase._conn.execute(f"DROP TABLE {table.name()}_old;")
        BackendBase._conn.commit()

        return True
