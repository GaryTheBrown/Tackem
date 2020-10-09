'''SQLLite System'''
import sqlite3
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.sql.baseclass import SqlBaseClass

class SqlLite(SqlBaseClass):
    '''sqllite system'''

    __sql = None
    __conn = None

    def _startup(self):
        '''Setup SQLlite Here'''
        self.__conn = sqlite3.connect(PROGRAMCONFIGLOCATION + '/Tackem.db')
        self.__sql = self.__conn.cursor()

    def _shutdown(self):
        '''Shutdown the System Here'''
        # save any changes to the file
        self.__conn.commit()
        # close the connection
        self.__conn.close()

    def _check_version_table_exists(self) -> bool:
        '''returns if the table_version exists'''
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name='table_version';"
        return bool(self._trusted_get(command, False))

    def _trusted_call(self, call: str):
        '''Trusted Calls can send the command in a string to here for execution'''
        self.__conn.commit()
        self.__sql.execute(call)
        self.__conn.commit()

    def _trusted_get(self, call: str, return_dict: bool = True) -> list:
        '''Grab a list of the tables'''
        self.__conn.commit()
        self.__sql.execute(call)
        self.__conn.commit()

        return_data = self.__sql.fetchall()
        if return_dict:
            col_name_list = [tuple[0] for tuple in self.__sql.description]
            full_return_data = []
            for row in return_data:
                return_dict = {}
                for count, key in enumerate(col_name_list):
                    return_dict[key] = row[count]
                full_return_data.append(return_dict)
            return full_return_data
        return return_data

    def _update_table(self, table_name: str, data: list, version: int) -> bool:
        '''Update the table with the informaiton provided'''

        # first move the current table to a new name
        command1 = "ALTER TABLE " + table_name + " RENAME TO " + table_name + "_old;"
        self._trusted_call(command1)

        # make the new version of the table
        self._add_table(table_name, data, version, False)

        # move Data across to new table
        command_get_old_table_columns = f"PRAGMA table_info({table_name}_old);"
        returned_data_temp_old = self._trusted_get(
            command_get_old_table_columns, False)
        command_get_new_table_columns = f"PRAGMA table_info({table_name});"
        returned_data_temp_new = self._trusted_get(
            command_get_new_table_columns, False)

        links = {}
        for new_column in returned_data_temp_new:
            for i, old_column in enumerate(returned_data_temp_old):
                if new_column[1] == old_column[1]:  # compare name
                    links[new_column[1]] = [True, i]

        for i, new_column in enumerate(returned_data_temp_new):
            if new_column[1] in links:  # if column is already linked skip it in this run
                continue
            if not new_column[4] is None:
                links[new_column[1]] = None
            else:  # if there is no default check if NULLABLE
                if not new_column[3]:
                    links[new_column[1]] = [False, None]
                else:  # Get Variable type and return a value to fill in here.
                    links[new_column[1]] = [False, data[i].get_default_value()]

        # create insert command here
        rows = self._trusted_get(f"SELECT * FROM {table_name}_old;", False)
        for row in rows:
            values = []
            for key in links:
                if links[key] is None:
                    continue
                if links[key][0]:
                    temp_value = ""
                    if isinstance(row[links[key][1]], int):
                        temp_value = str(row[links[key][1]])
                    elif isinstance(row[links[key][1]], str):
                        temp_value = f"'{row[links[key][1]]}'"
                    elif row[links[key][1]] is None:
                        temp_value = "NULL"
                    values.append(temp_value)
                else:
                    temp_value = ""
                    if isinstance(links[key][1], int):
                        temp_value = str(links[key][1])
                    elif isinstance(links[key][1], str):
                        temp_value = f"'{links[key][1]}'"
                    elif links[key][1] is None:
                        temp_value = "NULL"
                    values.append(temp_value)

            self._trusted_call(
                f"INSERT INTO {table_name} ({', '.join(list(links.keys()))}) " \
                    + f"Values ({', '.join(values)})"
            )

        # update table_version
        self._trusted_call(
            f"UPDATE table_version SET version={str(version)} " \
                + f'WHERE name="{table_name}";'
        )

        # delete old table
        self._trusted_call(f"DROP TABLE {table_name}_old;")

        return True
