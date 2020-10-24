'''SQL MESSAGE SYSTEM DATA'''
from typing import List
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError

class SQLUpdate(SQLMessage):
    '''Update Rows Message'''

    def __init__(self, table: str, *wheres: List[Where], **key_values: dict):
        if not isinstance(table, str):
            raise SQLMessageError

        where_list = [where.query for where in wheres]
        set_values = [f"{key} = :{key}" for key in key_values]
        variables = {
            "table": table,
        }
        variables.update(key_values)

        super().__init__(
            f"UPDATE :table SET {', '.join(set_values)} WHERE {' AND '.join(where_list)}",
            variables
        )
