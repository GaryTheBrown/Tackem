'''SQL MESSAGE SYSTEM DATA'''
from libs.database.messages.sql_message import SQLMessage
from libs.exceptions import SQLMessageError

class SQLInsert(SQLMessage):
    '''Insert Message'''

    def __init__(self, table: str, **key_values: dict):
        if not isinstance(table, str):
            raise SQLMessageError

        key_values['table'] = table.name
        values = ', '.join([f":{key}" for key in key_values])
        fields = ', '.join(key_values.keys())

        super().__init__(f"INSERT INTO :table ({fields}) VALUES ({values});", key_values)
