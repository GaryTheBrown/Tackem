'''SQLLite System'''
import sqlite3
from libs.startup_arguments import ARGS
from .baseclass import MysqlBaseClass

class SqlLite(MysqlBaseClass):
    '''sqllite system'''
    _sql = None
    _conn = None

    def _startup(self):
        '''Setup SQLlite Here'''
        self._conn = sqlite3.connect(ARGS.home + '/Tackem.db')
        self._sql = self._conn.cursor()

    def _shutdown(self):
        '''Shutdown the System Here'''
        #save any changes to the file
        self._conn.commit()
        #close the connection
        self._conn.close()

    def _check_version_table_exists(self):
        '''returns if the table_version exists'''
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name='table_version';"
        return bool(self._trusted_get(command))

    def _trusted_call(self, call):
        '''Trusted Calls can send the command in a string to here for execution'''
        self._conn.commit()
        self._sql.execute(call)
        self._conn.commit()

    def _trusted_get(self, call):
        '''Grab a list of the tables'''
        self._conn.commit()
        self._sql.execute(call)
        self._conn.commit()

        return_data = self._sql.fetchall()
        col_name_list = [tuple[0] for tuple in self._sql.description]
        full_return_data = []
        for row in return_data:
            return_dict = {}
            for count, key in enumerate(col_name_list):
                return_dict[key] = row[count]
            full_return_data.append(return_dict)
        return full_return_data

    def _update_table(self, table_name, data, version):
        '''Update the table with the informaiton provided'''

        #first move the current table to a new name
        command1 = "ALTER TABLE " + table_name + " RENAME TO " + table_name + "_old;"
        self._trusted_call(command1)

        #make the new version of the table
        self._add_table(table_name, data, version, False)

        #move Data across to new table
        command_get_old_table_columns = "PRAGMA table_info(" + table_name + "_old);"
        returned_data_temp_old = self._trusted_get(command_get_old_table_columns)
        command_get_new_table_columns = "PRAGMA table_info(" + table_name + ");"
        returned_data_temp_new = self._trusted_get(command_get_new_table_columns)

        links = {}
        for new_column in returned_data_temp_new:
            for i, old_column in enumerate(returned_data_temp_old):
                if new_column[1] == old_column[1]:#compare name
                    links[new_column[1]] = [True, i]

        for i, new_column in enumerate(returned_data_temp_new):
            if new_column[1] in links:#if column is already linked skip it in this run
                continue
            if not new_column[4] is None:
                links[new_column[1]] = None
            else: #if there is no default check if NULLABLE
                if not new_column[3]:
                    links[new_column[1]] = [False, None]
                else: # Get Variable type and return a value to fill in here.
                    links[new_column[1]] = [False, data[i].get_default_value()]

        #create insert command here
        insert = "INSERT INTO " + table_name + " (" + ", ".join(list(links.keys())) + ") VALUES "

        command_select_all_from_table = "SELECT * FROM " + table_name + "_old;"
        rows = self._trusted_get(command_select_all_from_table)
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
                        temp_value = "'" + row[links[key][1]] + "'"
                    elif isinstance(row[links[key][1]], None):
                        temp_value = "NULL"
                    values.append(temp_value)
                else:
                    temp_value = ""
                    if isinstance(links[key][1], int):
                        temp_value = str(links[key][1])
                    elif isinstance(links[key][1], str):
                        temp_value = "'" + links[key][1] + "'"
                    elif isinstance(links[key][1], None):
                        temp_value = "NULL"
                    values.append(temp_value)

            row_to_insert = insert + "(" + ", ".join(values) + ");"
            self._trusted_call(row_to_insert)

        #update table_version
        update_table_version = 'UPDATE table_version SET version=' + str(version)
        update_table_version += ' Where name="' + table_name + '";'
        self._trusted_call(update_table_version)

        #delete old table
        command_delete_table = "DROP TABLE " + table_name + "_old;"
        self._trusted_call(command_delete_table)

        return True
