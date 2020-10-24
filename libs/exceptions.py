'''Custom Exceptions'''

class TableError(Exception):
    '''Error in a Table'''

class ColumnNotFoundError(TableError):
    '''Column Has Not Been Found in the Table'''

class DatabaseError(Exception):
    '''Database Error'''

class TableCheckFailure(DatabaseError):
    '''Table Check Failure'''

class QueryError(Exception):
    '''Query Errors'''

class ConditionError(QueryError):
    '''Error in the Condition'''

class SQLMessageError(Exception):
    '''SQL Message Error'''
