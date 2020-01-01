'''SQL System'''
from config_data import CONFIG
from libs.sql.baseclass import SqlBaseClass
from libs.sql.mysql import MySql
from libs.sql.sqllite import SqlLite


def setup_db():
    '''basic function to load up the DB'''
    sql = None
    if CONFIG['database']['mode'].value.lower() == 'sqlite3':
        sql = SqlLite()
    # elif CONFIG['database']['mode'].lower() == 'mysql':
    #     sql = Mysql
    else:
        print(CONFIG['database']['mode'])
    return sql
