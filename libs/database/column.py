'''Column Defenition Stuff Useful for updating tables'''
from typing import Optional, Any
from datetime import datetime, date, time
import json

class Column:
    '''Column'''

    TYPE_BIT = "bit"
    TYPE_TINYINT = "tinyint"
    TYPE_SMALLINT = "smallint"
    TYPE_INT = "int"
    TYPE_MEDIUMINT = "mediumint"
    TYPE_INTEGER = "integer"
    TYPE_BIGINT = "bigint"
    TYPE_REAL = "real"
    TYPE_DOUBLE = "double"
    TYPE_FLOAT = "float"
    TYPE_DECIMAL = "decimal"
    TYPE_NUMERIC = "numeric"
    TYPE_CHAR = "char"
    TYPE_VARCHAR = "varchar"
    TYPE_BINARY = "binary"
    TYPE_VARBINARY = "varbinary"
    TYPE_TINYBLOB = "tinyblob"
    TYPE_BLOB = "blob"
    TYPE_MEDIUMBLOB = "mediumblob"
    TYPE_LONGBLOB = "longblob"
    TYPE_TINYTEXT = "tinytext"
    TYPE_TEXT = "text"
    TYPE_MEDIUMTEXT = "mediumtext"
    TYPE_LONGTEXT = "longtext"
    TYPE_DATE = "date"
    TYPE_TIME = "time"
    TYPE_TIMESTAMP = "timestamp"
    TYPE_DATETIME = "datetime"
    TYPE_YEAR = "year"
    TYPE_ENUM = "enum"
    TYPE_SET = "set"
    TYPE_JSON = "json"

    __types = {
        # bool
        "bit": 0,
        # ints
        "tinyint": 1, "smallint": 1, "int": 1, "mediumint": 1, "integer": 1, "bigint": 1,
        #float
        "real": 2, "double": 2, "float": 2, "decimal": 2, "numeric": 2,

        # text
        "char": 3, "varchar": 3, "binary": 3, "varbinary": 3, "tinyblob": 3, "blob": 3,
        "mediumblob": 3, "longblob": 3, "tinytext": 3, "text": 3, "mediumtext": 3, "longtext": 3,
        # special
        "date": 4, "time": 5, "timestamp": 6, "datetime": 7,
        "year": 8, "enum": 9, "set": 10, "json": 11
    }

    def __init__(
            self,
            name: str,
            variable_type: str,
            primary_key: bool = False,
            unique: bool = False,
            not_null: bool = False,
            default: Any = None,
            default_raw: bool = False,
            size: Optional[int] = None,
            decimal: Optional[int] = None,
            unsigned: bool = False,
            auto_increment: bool = False,
    ):
        self.__name = name
        self.__type = variable_type
        self.__primary_key = bool(primary_key)
        self.__unique = bool(unique)
        self.__not_null = bool(not_null)
        self.__default = default
        self.__default_raw = bool(default_raw)
        self.__size = size
        self.__decimal = decimal
        self.__unsigned = bool(unsigned)
        self.__auto_increment = bool(auto_increment)

    @property
    def name(self):
        '''returns the name'''
        return self.__name

    @property
    def variable_type(self):
        '''returns the variable_type'''
        return self.__type

    @property
    def primary_key(self):
        '''returns the primary_key'''
        return self.__primary_key

    @property
    def unique(self):
        '''returns the unique'''
        return self.__unique

    @property
    def not_null(self):
        '''returns the not_null'''
        return self.__not_null

    @property
    def default(self):
        '''returns the default'''
        return self.__default

    @property
    def default_raw(self):
        '''returns the default_raw'''
        return self.__default_raw

    @property
    def size(self):
        '''returns the size'''
        return self.__size

    @property
    def decimal(self):
        '''returns the decimal'''
        return self.__decimal

    @property
    def unsigned(self):
        '''returns the unsigned'''
        return self.__unsigned

    @property
    def auto_increment(self):
        '''returns the auto_increment'''
        return self.__auto_increment

    def check_value(self, value: Any):
        '''checks the value is correct depending on the type set will throw errors if wrong'''
        if (self.__types[self.__type] == 0 and isinstance(value, bool)) \
        or (self.__types[self.__type] == 1 and isinstance(value, int)) \
        or (self.__types[self.__type] == 2 and isinstance(value, float)) \
        or (self.__types[self.__type] == 3 and isinstance(value, str)) \
        or (self.__types[self.__type] == 4 and isinstance(value, date)) \
        or (self.__types[self.__type] == 5 and isinstance(value, time)) \
        or (self.__types[self.__type] == 6 and isinstance(value, int)) \
        or (self.__types[self.__type] == 7 and isinstance(value, datetime)) \
        or (self.__types[self.__type] == 8 and isinstance(value, int) and 9999 >= value >= 0) \
        or (self.__types[self.__type] == 9 and isinstance(value, str)) \
        or (self.__types[self.__type] == 10 and isinstance(value, str)):
            return
        if self.__types[self.__type] == 11:
            if isinstance(value, str):
                try:
                    json.loads(value)
                    return
                except:
                    raise ValueError(f"{self.__name} has Invalid Json String")
            if isinstance(value, (list, dict)):
                try:
                    json.dumps(value)
                    return
                except:
                    raise ValueError(f"{self.__name} cannot convert to Json String")

        raise ValueError(f"{self.__name} Expecting {self.__type} found {type(value)}")

    def create_string(self) -> str:
        '''turns Column info into a string for commands'''
        return_string = f'"{self.__name}" {self.__type.upper()}'
        if self.__size and self.__decimal:
            return_string += f"({self.__size}, {self.__decimal})"
        elif self.__size:
            return_string += f"({self.__size})"
        return_string += " UNSIGNED" if self.__unsigned else ""
        return_string += " PRIMARY KEY" if self.__primary_key else ""
        return_string += " NOT NULL" if self.__not_null else ""
        return_string += " UNIQUE" if self.__unique else ""
        return_string += " AUTOINCREMENT" if self.__auto_increment else ""
        if self.__default is not None:
            return_string += " DEFAULT "
            if isinstance(self.__default, str):
                if self.__default_raw:
                    return_string += self.__default
                else:
                    return_string += f"'{self.__default}'"
            elif isinstance(self.__default, int):
                return_string += str(self.__default)
            elif isinstance(self.__default, bool):
                return_string += '"True"' if self.__default else '"False"'
        return return_string
