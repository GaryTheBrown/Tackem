'''SQL MESSAGE SYSTEM DATA'''
from typing import List
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError

class SQLDelete(SQLMessage):
    '''Delete Message'''

    def __init__(self, table: str, *wheres: Where):
        if not isinstance(table, str):
            raise SQLMessageError

        if len(wheres) == 0:
            return

        where_list = [where.query for where in wheres]
        super().__init__(f"DELETE FROM {table} WHERE {' AND '.join(where_list)}")
