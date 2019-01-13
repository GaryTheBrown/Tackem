'''MySQL Abstract Class System'''
#import itertools
import threading
import json
from abc import ABCMeta, abstractmethod
from .column import Column
from .sql_message import SQLMessage

class MysqlBaseClass(metaclass=ABCMeta):
    '''base class of database access'''

    _event_lock = threading.Event()
    _event_list = []
    _event_list_lock = threading.Lock()

    _thread_run = True

    def __init__(self):
        '''INIT'''
        self._thread = threading.Thread(target=self._run, args=())
        self._thread.setName("SQL")

    def start_thread(self):
        '''start the thread'''
        if not self._thread.is_alive():
            self._thread.start()
            return True
        return False

    def stop_thread(self):
        '''stop the thread'''
        if self._thread.is_alive():
            self._thread_run = False
            self._event_lock.set()
            self._thread.join()

    def get_thread_run(self):
        '''return if thread is running'''
        return self._thread.is_alive()

    def call(self, system_name, call):
        '''Function to call the sql through threadding'''
        return self._call(SQLMessage(system_name, command=call))

    def get(self, system_name, call):
        '''Function to call the sql through threadding'''
        return self._call(SQLMessage(system_name, command=call, return_data=[]))

    def table_check(self, system_name, table_name, data, version):
        '''Function to do a table check'''
        return self._call(SQLMessage(system_name,
                                     special_command="tablecheck",
                                     table_name=table_name,
                                     data=data,
                                     version=version))

    def table_has_row(self, system_name, table_name, dict_of_queries):
        '''Check if the Table has row by looking for all the queries'''
        queries = []
        for key in dict_of_queries:
            query = key + "="
            if isinstance(dict_of_queries[key], int):
                query += str(dict_of_queries[key])
            elif isinstance(dict_of_queries[key], bool):
                if dict_of_queries[key]:
                    query += '"True"'
                else:
                    query += '"False"'
            else:
                query += '"' + dict_of_queries[key] + '"'
            queries.append(query)

        command = "SELECT id FROM " + table_name
        command += " WHERE " + " AND ".join(queries) + ";"
        return_value = self._call(SQLMessage(system_name, command=command, return_data=[]))
        if return_value:
            if isinstance(return_value, list):
                if isinstance(return_value[0], tuple):
                    if len(return_value[0]) == 1:
                        return return_value[0][0]
        return 0

    def insert(self, system_name, table_name, dict_of_values):
        '''insert data into a table'''
        keys = list(dict_of_values.keys())
        command = "INSERT INTO " + table_name + " (" + ", ".join(keys) + ") VALUES ("
        values = []
        for key in dict_of_values:
            temp_value = ""
            if isinstance(dict_of_values[key], int):
                temp_value = str(dict_of_values[key])
            elif isinstance(dict_of_values[key], str):
                temp_value = "'" + dict_of_values[key] + "'"
            elif dict_of_values[key] is None:
                temp_value = "NULL"
            elif isinstance(dict_of_values[key], bool):
                if dict_of_values[key]:
                    temp_value += '"True"'
                else:
                    temp_value += '"False"'
            elif isinstance(dict_of_values[key], (dict, list)):
                temp_value = "'" + json.dumps(dict_of_values[key], ensure_ascii=False) + "'"
            values.append(temp_value)
        command += ", " .join(values) + ");"
        return self._call(SQLMessage(system_name, command=command))

    def select(self, system_name, table_name, dict_of_values, list_of_returns=None):
        '''select data from a table'''
        returns = "*"
        if isinstance(list_of_returns, list):
            returns = ", ".join(list_of_returns)
        elif isinstance(list_of_returns, str):
            returns = list_of_returns
        command = "SELECT " + returns + " FROM " + table_name + " WHERE "
        values = []
        for key in dict_of_values:
            temp_value = ""
            if isinstance(dict_of_values[key], bool):
                if dict_of_values[key]:
                    temp_value += '"True"'
                else:
                    temp_value += '"False"'
            elif isinstance(dict_of_values[key], int):
                temp_value = str(dict_of_values[key])
            elif isinstance(dict_of_values[key], str):
                temp_value = "'" + dict_of_values[key] + "'"
            elif dict_of_values[key] is None:
                temp_value = "NULL"

            elif isinstance(dict_of_values[key], dict):
                temp_value = '"' + json.dumps(dict_of_values[key], ensure_ascii=False) + '"'
            values.append(key + "=" + temp_value)
        command += " AND " .join(values) + ";"
        return self._call(SQLMessage(system_name, command=command, return_data=[]))

    def select_by_row(self, system_name, table_name, row_id, list_of_returns=None):
        '''insert data into a table'''
        returns = "*"
        if isinstance(list_of_returns, list):
            returns = ", ".join(list_of_returns)
        elif isinstance(list_of_returns, str):
            returns = list_of_returns
        command = "SELECT " + returns + " FROM " + table_name + " WHERE id=" + str(row_id) + ";"
        return self._call(SQLMessage(system_name, command=command, return_data=[]))

    def update(self, system_name, table_name, row_id, dict_of_values):
        '''update a row'''
        command = "UPDATE " + table_name + " SET "
        values = []
        for key in dict_of_values:
            temp_value = ""
            if isinstance(dict_of_values[key], int):
                temp_value = str(dict_of_values[key])
            elif isinstance(dict_of_values[key], str):
                temp_value = "'" + dict_of_values[key] + "'"
            elif dict_of_values[key] is None:
                temp_value = "NULL"
            elif isinstance(dict_of_values[key], bool):
                if dict_of_values[key]:
                    temp_value += '"True"'
                else:
                    temp_value += '"False"'
            elif isinstance(dict_of_values[key], dict):
                temp_value = '"' + json.dumps(dict_of_values[key], ensure_ascii=False) + '"'
            values.append(key + "=" + temp_value)
        command += ", " .join(values) + " WHERE id=" + str(row_id) + ";"
        return self._call(SQLMessage(system_name, command=command))

    def _call(self, job):
        '''underlying call'''
        with self._event_list_lock:
            self._event_list.append(job)
        self._event_lock.set()
        job.event_wait()
        if isinstance(job.return_data(), list):
            return job.return_data()
        return True

##########
##THREAD##
##########

    def _run(self):
        '''Threadded Run'''
        self._startup()
        self._create_main_tables()
        while self._thread_run:
            self._event_lock.wait()
            while self._event_list:
                with self._event_list_lock:
                    job = self._event_list.pop()
                if isinstance(job, SQLMessage):
                    if job.special_command() is not None:
                        if job.special_command() == "tablecheck":
                            job.set_return_data(self._table_check(job.table_name(),
                                                                  job.data(),
                                                                  job.version()))
                    else: #None Special command just simple command
                        #Means command is simple command with or without return
                        if isinstance(job.return_data(), list):
                            job.set_return_data(self._trusted_get(job.command()))
                        else:
                            self._trusted_call(job.command())


                    #finally release the waiting thread
                    job.event_set()
                else:
                    print("WTF IS PASSED IN???", type(job), job)

            self._event_lock.clear()
        self._shutdown()

    @abstractmethod
    def _startup(self):
        '''Setup the System Here'''
        pass

    @abstractmethod
    def _shutdown(self):
        '''Shutdown the System Here'''
        pass

    @abstractmethod
    def _check_version_table_exists(self):
        '''returns if the table_version exists'''
        pass

    @abstractmethod
    def _trusted_call(self, call):
        '''Trusted Calls can send the command in a string to here for execution'''
        pass

    @abstractmethod
    def _trusted_get(self, call):
        '''Grab a list of the tables'''
        pass

    @abstractmethod
    def _update_table(self, table_name, data, version):
        '''Update the table with the informaiton provided'''
        pass

    def _create_main_tables(self):
        '''Creates Tables'''
        if not self._check_version_table_exists():#TABLE_VERSION
            table_version_columns = [
                Column("id", "integer", primary_key=True, not_null=True),
                Column("name", "text", unique=True, not_null=True),
                Column("version", "integer", not_null=True)
            ]
            self._add_table("table_version", table_version_columns, 0, False)

    def _table_check(self, table_name, data, version):
        '''checks if the table exists adds it if it doesn't and update it if needed'''
        table_version = self._table_exists(table_name)
        if table_version == version:
            return True
        elif table_version == 0:
            return self._add_table(table_name, data, version)
        elif table_version < version:
            return self._update_table(table_name, data, version)
        return False

    def _table_exists(self, table_name):
        '''Check if Table Exists'''
        command = 'SELECT version FROM table_version WHERE name="' + table_name + '";'
        info = self._trusted_get(command)
        if not info:
            return 0
        return info[0][0]

    def _add_table(self, table_name, data, version, update_table=True):
        ''' Adds Table to the DB and then adds it into the table version DB'''
        array_of_variables = list(map(lambda v: v.to_string(), data))
        variables = ",".join(array_of_variables)
        create_table = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + variables + ");"
        self._trusted_call(create_table)
        if update_table:
            update_table_call = "INSERT INTO table_version (name, version) VALUES ('"
            update_table_call += table_name +"', " + str(version) + ");"
            self._trusted_call(update_table_call)
        return True
