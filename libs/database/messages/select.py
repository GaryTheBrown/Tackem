"""SQL MESSAGE SYSTEM DATA"""
from typing import List
from typing import Optional

from libs.database.messages.sql_message import SQLMessage
from libs.database.table import Table
from libs.database.where import Where
from libs.exceptions import SQLMessageError


class SQLSelect(SQLMessage):
    """Select Message"""

    def __init__(self, table: Table, *wheres: Where, returns: Optional[List[str]] = None):
        if not isinstance(table, Table):
            raise SQLMessageError

        if returns is None:
            returns = ["*"]

        if len(wheres) == 0 and table.soft_delete is False:
            super().__init__(f"SELECT {', '.join(returns)} FROM {table.name()}")
            return

        where_list = [where.query for where in wheres]
        if table.soft_delete:
            where_list.append(Where("deleted_at", 0).query)

        super().__init__(
            f"SELECT {', '.join(returns)} FROM {table.name()} WHERE {' AND '.join(where_list)}"
        )
