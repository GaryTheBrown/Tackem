"""SQL MESSAGE SYSTEM DATA"""
from libs.database.messages.sql_message import SQLMessage
from libs.database.table import Table
from libs.exceptions import SQLMessageError


class SQLTable(SQLMessage):
    """Table Checker Message"""

    def __init__(self, table: Table):
        if not isinstance(table, Table):
            raise SQLMessageError
        super().__init__(table)
