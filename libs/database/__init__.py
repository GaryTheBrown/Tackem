'''SQL System'''
from typing import Any, Union
from config_data import CONFIG
from libs.database.messages.sql_message import SQLMessage
from libs.database.table import Table
from libs.database.backend.sqlite import SQLite
from libs.database.backend.mysql import MySQL

class Database:
    '''SQL System'''
    __sql_system = None

    @classmethod
    def setup_db(cls):
        '''basic function to load up the DB'''
        if CONFIG['database']['mode'].value.lower() == 'sqlite3':
            cls.__sql_system = SQLite()
        elif CONFIG['database']['mode'].lower() == 'mysql':
            cls.__sql_system = MySQL()
        else:
            print(CONFIG['database']['mode'].value)

    @classmethod
    def start_sql(cls):
        '''starts the SQL System'''
        cls.__sql_system.start_thread()

    @classmethod
    def stop_sql(cls):
        '''stops the SQL System'''
        if cls.__sql_system is not None:
            cls.__sql_system.stop_thread()

    @classmethod
    def call(cls, message: SQLMessage) -> Any:
        '''function to pass the query/table through to the backend thread'''
        return cls.__sql_system.call(message)
