'''SQL System'''
from .baseclass import MysqlBaseClass
from .mysql import MySql
from .sqllite import SqlLite

def setup_db(config):
    '''basic function to load up the DB'''
    sql = None
    if config['mode'] == 'SQLite3':
        sql = SqlLite()
    # elif config['mode'] == 'MYSQL':
    #     sql = MySql()
    else:
        print(config['mode'])
    sql.start_thread()
    return sql