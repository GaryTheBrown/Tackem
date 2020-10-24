'''SQL MESSAGE SYSTEM DATA'''
from typing import List, Optional
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError

class SQLSelect(SQLMessage):
    '''Select Message'''

    def __init__(self, table: str, *wheres: List[Where], returns: Optional[List[str]] = None):
        if not isinstance(table, str):
            raise SQLMessageError

        if returns is None:
            returns = ["*"]

        if len(wheres) == 0:
            super().__init__(
                f"SELECT ? FROM {table}",
                (
                    ", ".join(returns),
                )
            )
            return

        where_list = [where.query for where in wheres]
        variables = {
            "returns": ", ".join(returns),
        }
        for where in wheres:
            variables[where.key] = where.value
        super().__init__(
            f"SELECT :returns FROM {table} WHERE {' AND '.join(where_list)}",
            tuple(variables)
        )
