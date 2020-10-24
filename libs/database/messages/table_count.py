'''SQL MESSAGE SYSTEM DATA'''
from libs.database.messages.sql_message import SQLMessage
from libs.exceptions import SQLMessageError

class SQLTableCount(SQLMessage):
    '''Table Count Rows Message'''
    def __init__(self, table: str):
        if not isinstance(table, str):
            raise SQLMessageError

        super().__init__(f"SELECT COUNT(*) FROM {table}")
