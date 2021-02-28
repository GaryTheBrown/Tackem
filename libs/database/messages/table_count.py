'''SQL MESSAGE SYSTEM DATA'''
from libs.database.table import Table
from libs.database.messages.sql_message import SQLMessage
from libs.exceptions import SQLMessageError

class SQLTableCount(SQLMessage):
    '''Table Count Rows Message'''
    def __init__(self, table: Table):
        if not isinstance(table, Table):
            raise SQLMessageError

        super().__init__(f"SELECT COUNT(*) FROM {table.name()}")
