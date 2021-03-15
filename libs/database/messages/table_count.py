"""SQL MESSAGE SYSTEM DATA"""
from libs.database.messages.sql_message import SQLMessage
from libs.database.table import Table
from libs.database.where import Where
from libs.exceptions import SQLMessageError


class SQLTableCount(SQLMessage):
    """Table Count Rows Message"""

    def __init__(self, table: Table):
        if not isinstance(table, Table):
            raise SQLMessageError
        if table.soft_delete:
            soft_delete = Where("deleted_at", 0).query
            super().__init__(f"SELECT COUNT(*) FROM {table.name()} WHERE {soft_delete}")
        else:
            super().__init__(f"SELECT COUNT(*) FROM {table.name()}")
