"""SQL MESSAGE SYSTEM DATA"""
from libs.database.table import Table
import time
from typing import Any
from libs.database.messages.sql_message import SQLMessage
from libs.database.where import Where
from libs.exceptions import SQLMessageError


class SQLUpdate(SQLMessage):
    """Update Rows Message"""

    def __init__(self, table: Table, *wheres: Where, **key_values: Any):
        if not isinstance(table, Table):
            raise SQLMessageError

        where_list = [where.query for where in wheres]
        if table.soft_delete:
            where_list.append(Where("deleted_at", 0).query)
        set_values = [f"{key} = '{key_values[key]}'" for key in key_values]
        set_values.append(f"updated_at = {int(time.time())}")

        super().__init__(
            f"UPDATE {table.name()} SET {', '.join(set_values)} WHERE {' AND '.join(where_list)}"
        )
