"""SQL MESSAGE SYSTEM DATA"""
import time
from libs.database.table import Table
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError


class SQLDelete(SQLMessage):
    """Delete Message"""

    def __init__(self, table: Table, *wheres: Where):
        if not isinstance(table, Table):
            raise SQLMessageError

        if len(wheres) == 0:
            return

        where_list = [where.query for where in wheres]
        if table.soft_delete:
            set = f"deleted_at = {int(time.time())}"
            where = " AND ".join(where_list)
            super().__init__(f"UPDATE {table.name()} SET {set} WHERE {where}")
        else:
            super().__init__(f"DELETE FROM {table.name()} WHERE {' AND '.join(where_list)}")
