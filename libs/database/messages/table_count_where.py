'''SQL MESSAGE SYSTEM DATA'''
from libs.database.table import Table
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError

class SQLTableCountWhere(SQLMessage):
    '''Table Count Rows Message'''

    def __init__(self, table: Table, *wheres: Where):
        if not isinstance(table, Table):
            raise SQLMessageError

        where_list = [where.query for where in wheres]

        super().__init__(f"SELECT COUNT(*) FROM {table.name()} WHERE {' AND '.join(where_list)}")
