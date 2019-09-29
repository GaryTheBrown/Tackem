'''SQL System'''
from .baseclass import SqlBaseClass
from .mysql import MySql
from .sqllite import SqlLite

def setup_db(config):
    '''basic function to load up the DB'''
    sql = None
    if config['mode'].lower() == 'sqlite3':
        sql = SqlLite()
    # elif config['mode'].lower() == 'mysql':
    #     sql = Mysql
    else:
        print(config['mode'])
    return sql
