'''MYSQL System'''
import mysql.connector
from data.config import CONFIG
from libs.database.backend.base import BackendBase
from libs.database.table import Table


class MySQL(BackendBase):
    '''MySQL system'''

    def __startup(self):
        '''Setup SQLlite Here'''
        config = {
            'user': CONFIG['database']['mysql']['username'].value,
            'password': CONFIG['database']['mysql']['password'].value,
            'host': CONFIG['database']['mysql']['host'].value,
            'port': CONFIG['database']['mysql']['port'].value,
            'database': CONFIG['database']['mysql']['database'].value,
            'raise_on_warnings': True
        }

        try:
            super()._conn = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        # if not self.__check_version_table_exists():
        #     self.__add_table(TABLE_VERSION_DB, False)

    def __shutdown(self):
        '''Shutdown the System Here'''
        super()._conn.close()

    def __get_cursor(self):
        '''returns a sql cursor'''
        return super()._conn.cursor(dictionary=True)

    def __table_check(self, table: Table) -> bool:
        '''checks if the table exists adds it if it doesn't and update it if needed'''
