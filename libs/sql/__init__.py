'''SQL System'''
from typing import Union
from config_data import CONFIG
from libs.sql.baseclass import SqlBaseClass
from libs.sql.mysql import MySql
from libs.sql.sqllite import SqlLite


class Database:
    '''SQL System'''
    __sql = None

    @classmethod
    def setup_db(cls):
        '''basic function to load up the DB'''
        if CONFIG['database']['mode'].value.lower() == 'sqlite3':
            cls.__sql = SqlLite()
        # elif CONFIG['database']['mode'].lower() == 'mysql':
        #     cls.__sql = Mysql
        else:
            print(CONFIG['database']['mode'].value)

    @classmethod
    def sql(cls) -> SqlBaseClass:
        '''returns the sql'''
        return cls.__sql

    @classmethod
    def start_sql(cls):
        '''starts the SQL System'''
        cls.__sql.start_thread()

    @classmethod
    def stop_sql(cls):
        '''stops the SQL System'''
        if cls.__sql is not None:
            cls.__sql.stop_thread()
