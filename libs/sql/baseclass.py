'''SQL Abstract Class System'''
from typing import Any, Optional
import threading
import json
from abc import ABCMeta, abstractmethod
from libs.sql.column import Column
from libs.sql.sql_message import SQLMessage


class SqlBaseClass(metaclass=ABCMeta):
    '''base class of database access'''


    _event_lock = threading.Event()
    _event_list = []
    _event_list_lock = threading.Lock()

    _thread_run = True


    def __init__(self):
        '''INIT'''
        self._thread = threading.Thread(target=self.__run, args=())
        self._thread.setName("SQL")


    def start_thread(self) -> bool:
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


    def get_thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()


    def call(self, system_name: str, call: str) -> Any:
        '''Function to call the sql through threadding'''
        return self.__call(
            SQLMessage(
                system_name,
                command=call
            )
        )


    def get(self, system_name: str, call: str) -> Any:
        '''Function to call the sql through threadding'''
        return self.__call(
            SQLMessage(
                system_name,
                command=call,
                return_data=[]
            )
        )


    def table_check(self, system_name: str, table_name: str, data: list, version: int) -> Any:
        '''Function to do a table check'''
        return self.__call(
            SQLMessage(
                system_name,
                special_command="tablecheck",
                table_name=table_name,
                data=data,
                version=version
            )
        )


    def table_checks(self, system_name: str, data: list) -> Any:
        '''Function to do a table check from a dict'''
        return self.table_check(system_name, data["name"], data["data"], data["version"])


    def table_has_row(self, system_name: str, table_name: str, dict_of_queries: dict) -> int:
        '''Check if the Table has row by looking for all the queries'''
        queries = []
        for key in dict_of_queries:
            queries.append(key + " = " + self.__convert_var(dict_of_queries[key]))

        command = "SELECT id FROM " + table_name
        command += " WHERE " + " AND ".join(queries) + ";"
        if return_value := self.__call(SQLMessage(system_name, command=command, return_data=[])):
            if isinstance(return_value, list) and len(return_value) == 1:
                if isinstance(return_value[0], dict):
                    return return_value[0]['id']
        return 0


    def insert(self, system_name: str, table_name: str, dict_of_values: dict) -> Any:
        '''insert data into a table'''
        keys = list(dict_of_values.keys())
        command = "INSERT INTO " + table_name + " (" + ", ".join(keys) + ") VALUES ("
        values = []
        for key in dict_of_values:
            values.append(self.__convert_var(dict_of_values[key]))
        command += ", ".join(values) + ");"
        return self.__call(SQLMessage(system_name, command=command))


    def select(
            self,
            system_name: str,
            table_name: str,
            dict_of_values: Optional[dict] = None,
            list_of_returns: Optional[list] = None
    ) -> Any:
        '''select data from a table'''
        returns = "*"
        if isinstance(list_of_returns, list):
            returns = ", ".join(list_of_returns)
        elif isinstance(list_of_returns, str):
            returns = list_of_returns
        command = "SELECT " + returns + " FROM " + table_name
        if dict_of_values:
            command += " WHERE "
            values = []
            for key in dict_of_values:
                values.append(key + " = " + self.__convert_var(dict_of_values[key]))
            command += " AND ".join(values)
        command += ";"
        return self.__call(SQLMessage(system_name, command=command, return_data=[]))


    def select_like(
            self,
            system_name: str,
            table_name: str,
            dict_of_values: Optional[dict] = None,
            list_of_returns: Optional[list] = None
    ) -> Any:
        '''select data from a table'''
        returns = "*"
        if isinstance(list_of_returns, list):
            returns = ", ".join(list_of_returns)
        elif isinstance(list_of_returns, str):
            returns = list_of_returns
        command = "SELECT " + returns + " FROM " + table_name
        if dict_of_values:
            command += " WHERE "
            values = []
            for key in dict_of_values:
                values.append(key + " LIKE " + self.__convert_var(dict_of_values[key]))
            command += " AND ".join(values)
        command += ";"
        return self.__call(SQLMessage(system_name, command=command, return_data=[]))


    def count(self, system_name: str, table_name: str) -> Any:
        '''select data from a table'''
        command = "SELECT COUNT(*) FROM " + table_name + ";"
        return self.__call(SQLMessage(system_name, command=command, return_data=[],
                                      return_dict=False))[0][0]


    def count_where(self, system_name: str, table_name: str, dict_of_values: dict) -> Any:
        '''select data from a table'''
        command = "SELECT COUNT(*) FROM " + table_name + " WHERE "
        values = []
        for key in dict_of_values:
            values.append(key + " = " + self.__convert_var(dict_of_values[key]))
        command += " AND ".join(values) + ";"
        return self.__call(SQLMessage(system_name, command=command, return_data=[],
                                      return_dict=False))[0][0]


    def select_by_row(
            self,
            system_name: str,
            table_name: str,
            row_id: int,
            list_of_returns: Optional[list] = None
    ) -> Any:
        '''insert data into a table'''
        returns = "*"
        if isinstance(list_of_returns, list):
            returns = ", ".join(list_of_returns)
        elif isinstance(list_of_returns, str):
            returns = list_of_returns
        command = "SELECT " + returns + " FROM " + table_name + " WHERE id=" + str(row_id) + ";"
        return_data = self.__call(SQLMessage(system_name, command=command, return_data=[]))
        if return_data:
            return return_data[0]
        return False


    def update(self, system_name: str, table_name: str, row_id: int, dict_of_values: dict) -> Any:
        '''update a row'''
        command = "UPDATE " + table_name + " SET "
        values = []
        for key in dict_of_values:
            values.append(key + " = " + self.__convert_var(dict_of_values[key]))
        command += ", ".join(values) + " WHERE id=" + str(row_id) + ";"
        return self.__call(SQLMessage(system_name, command=command))


    def delete_row(self, system_name: str, table_name: str, row_id: int) -> Any:
        '''delete a row by id'''
        command = "DELETE FROM " + table_name + " WHERE id=" + str(row_id) +";"
        return self.__call(SQLMessage(system_name, command=command))


    def delete_where(self, system_name: str, table_name: str, dict_of_values: dict) -> Any:
        '''delete a row by id'''
        command = "DELETE FROM " + table_name + " WHERE "
        values = []
        for key in dict_of_values:
            values.append(key + " = " + self.__convert_var(dict_of_values[key]))
        command += " AND ".join(values) + ";"
        return self.__call(SQLMessage(system_name, command=command))


    def __call(self, job: SQLMessage) -> Any:
        '''underlying call'''
        with self._event_list_lock:
            self._event_list.append(job)
        self._event_lock.set()
        job.event_wait()
        if isinstance(job.return_data, (list, dict)):
            return job.return_data
        return True


    def __convert_var(self, var: Any) -> str:
        '''convert the value'''
        if isinstance(var, bool):
            return '"True"' if var else '"False"'
        elif isinstance(var, int):
            return str(var)
        elif isinstance(var, str):
            return "'" + var + "'"
        elif var is None:
            return "NULL"
        elif isinstance(var, dict):
            return '"' + json.dumps(var, ensure_ascii=False) + '"'


##########
##THREAD##
##########


    def __run(self):
        '''Threadded Run'''
        self._startup()
        self.__create_main_tables()
        while self._thread_run:
            self._event_lock.wait()
            while self._event_list:
                with self._event_list_lock:
                    job = self._event_list.pop()
                if isinstance(job, SQLMessage):
                    if job.special_command is not None:
                        if job.special_command == "tablecheck":
                            job.set_return_data(self.__table_check(job.table_name,
                                                                   job.data,
                                                                   job.version))
                    else: #None Special command just simple command
                        #Means command is simple command with or without return
                        if isinstance(job.return_data, list):
                            print("1", job.command)
                            job.set_return_data(
                                self._trusted_get(job.command, job.return_dict)
                            )
                        else:
                            print("2", job.command)
                            self._trusted_call(job.command)


                    #finally release the waiting thread
                    job.event_set()
                else:
                    print("WTF IS PASSED IN???", type(job), job)

            self._event_lock.clear()
        self._shutdown()


    @abstractmethod
    def _startup(self):
        '''Setup the System Here'''


    @abstractmethod
    def _shutdown(self):
        '''Shutdown the System Here'''


    @abstractmethod
    def _check_version_table_exists(self) -> bool:
        '''returns if the table_version exists'''


    @abstractmethod
    def _trusted_call(self, call: str):
        '''Trusted Calls can send the command in a string to here for execution'''


    @abstractmethod
    def _trusted_get(self, call: str, return_dict: bool = True) -> list:
        '''Grab a list of the tables'''


    @abstractmethod
    def _update_table(self, table_name: str, data: list, version: int) -> bool:
        '''Update the table with the informaiton provided'''


    def __create_main_tables(self):
        '''Creates Tables'''
        if not self._check_version_table_exists():#TABLE_VERSION
            table_version_columns = [
                Column("id", "integer", primary_key=True, not_null=True),
                Column("name", "text", unique=True, not_null=True),
                Column("version", "integer", not_null=True)
            ]
            self._add_table("table_version", table_version_columns, 0, False)


    def __table_check(self, table_name: str, data: list, version: int) -> bool:
        '''checks if the table exists adds it if it doesn't and update it if needed'''
        table_version = self.__table_exists(table_name)
        if table_version == version:
            return True
        if table_version == 0:
            return self._add_table(table_name, data, version)
        if table_version < version:
            return self._update_table(table_name, data, version)
        return False


    def __table_exists(self, table_name: str) -> int:
        '''Check if Table Exists return version number'''
        command = 'SELECT version FROM table_version WHERE name="' + table_name + '";'
        if info := self._trusted_get(command):
            return info[0]['version']
        return 0


    def _add_table(
            self,
            table_name: str,
            data: list,
            version: int,
            update_table: bool = True
    ) -> bool:
        ''' Adds Table to the DB and then adds it into the table version DB'''
        array_of_variables = list(map(lambda v: v.to_string(), data))
        variables = ",".join(array_of_variables)
        create_table = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + variables + ");"
        self._trusted_call(create_table)
        if update_table:
            update_table__call = "INSERT INTO table_version (name, version) VALUES ('"
            update_table__call += table_name +"', " + str(version) + ");"
            self._trusted_call(update_table__call)
        return True
