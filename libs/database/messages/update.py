'''SQL MESSAGE SYSTEM DATA'''
import time
from typing import Any
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError

class SQLUpdate(SQLMessage):
    '''Update Rows Message'''

    def __init__(self, table: str, *wheres: Where, **key_values: Any):
        if not isinstance(table, str):
            raise SQLMessageError

        where_list = [where.query for where in wheres]
        set_values = [f"{key} = '{key_values[key]}'" for key in key_values]
        set_values.append(f"updated_at = {int(time.time())}")

        super().__init__(
            f"UPDATE {table} SET {', '.join(set_values)} WHERE {' AND '.join(where_list)}"
        )
