'''SQL MESSAGE SYSTEM DATA'''
from typing import List, Optional
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError

class SQLSelect(SQLMessage):
    '''Select Message'''

    def __init__(self, table: str, *wheres: Where, returns: Optional[List[str]] = None):
        if not isinstance(table, str):
            raise SQLMessageError

        if returns is None:
            returns = ["*"]

        if len(wheres) == 0:
            super().__init__(f"SELECT {', '.join(returns)} FROM {table}")
            return

        where_list = [where.query for where in wheres]
        super().__init__(
            f"SELECT {', '.join(returns)} FROM {table} WHERE {' AND '.join(where_list)}"
        )
