'''SQL System'''
from libs.database.backend.base import BackendBase
from typing import Any, Union
from data.config import CONFIG
from libs.database.messages.sql_message import SQLMessage
from libs.database.table import Table
from libs.database.backend.sqlite import SQLite
from libs.database.backend.mysql import MySQL


class Database:
    '''SQL System'''
    __sql_system: BackendBase = None

    @classmethod
    def start(cls):
        '''starts the SQL System'''
        if CONFIG['database']['mode'].value.lower() == 'sqlite3':
            cls.__sql_system = SQLite()
        # elif CONFIG['database']['mode'].lower() == 'mysql':
        #     cls.__sql_system = MySQL()
        else:
            print(CONFIG['database']['mode'].value)

        cls.__sql_system.start_thread()

    @classmethod
    def stop(cls):
        '''stops the SQL System'''
        if cls.__sql_system is not None:
            cls.__sql_system.stop_thread()

    @classmethod
    def call(cls, message: SQLMessage) -> Any:
        '''function to pass the query/table through to the backend thread'''
        return cls.__sql_system.call(message)

    @classmethod
    def count(cls, message: SQLMessage) -> int:
        '''quick count how many results'''
        cls.__sql_system.call(message)
        if isinstance(message.return_data, dict):
            return 1
        return len(message.return_data)
