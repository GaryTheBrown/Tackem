'''SQL MESSAGE SYSTEM DATA'''
from typing import Any
from libs.database.messages.sql_message import SQLMessage
from libs.exceptions import SQLMessageError

class SQLInsert(SQLMessage):
    '''Insert Message'''

    def __init__(self, table: str, **key_values: Any):
        if not isinstance(table, str):
            raise SQLMessageError

        value_list = [f"'{str(item)}'" for item in key_values.values()]

        fields = ', '.join(key_values)

        super().__init__(f"INSERT INTO {table} ({fields}) VALUES ({', '.join(value_list)});")
