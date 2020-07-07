'''Column Defenition Stuff Useful for updating tables'''
from typing import Optional, Any
import time

class Column:
    '''Column'''

    __variable_types = {
        # bool
        "bit": 0,
        # ints
        "tinyint": 1, "smallint": 1, "int": 1, "mediumint": 1, "integer": 1, "bigint": 1,
        "real": 1, "double": 1, "float": 1, "decimal": 1, "numeric": 1,
        # text
        "char": 2, "varchar": 2, "binary": 2, "varbinary": 2, "tinyblob": 2, "blob": 2,
        "mediumblob": 2, "longblob": 2, "tinytext": 2, "text": 2, "mediumtext": 2, "longtext": 2,
        # special
        "date": 3, "time": 4, "timestamp": 5, "datetime": 6,
        "year": 7, "enum": 8, "set": 9, "json": 10
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
            timestamp_update: bool = False
    ):
        self.__name = name
        self.__variable_type = variable_type
        self.__primary_key = bool(primary_key)
        self.__unique = bool(unique)
        self.__not_null = bool(not_null)
        self.__default = default
        self.__default_raw = bool(default_raw)
        self.__size = size
        self.__decimal = decimal
        self.__unsigned = unsigned
        self.__auto_increment = auto_increment
        self.__timestamp_update = timestamp_update

    def __repr__(self) -> str:
        '''print return'''
        return "Column(" + self.to_string() + ")"

    @property
    def name(self):
        '''returns the name'''
        return self.__name

    def to_string(self) -> str:
        '''turns Column info into a string for commands'''
        return_string = '"{}" {}'.format(self.__name, self.__variable_type)
        if self.__size and self.__decimal:
            return_string += "({}, {})".format(self.__size, self.__decimal)
        elif self.__size:
            return_string += "({})".format(self.__size)
        return_string += " UNSIGNED" if self.__unsigned else ""
        return_string += " PRIMARY KEY" if self.__primary_key else ""
        return_string += " NOT NULL" if self.__not_null else ""
        return_string += " UNIQUE" if self.__unique else ""
        return_string += " AUTO_INCREMENT" if self.__auto_increment else ""
        return_string += " ON UPDATE CURRENT_TIMESTAMP" if self.__timestamp_update else ""
        if self.__default is not None:
            return_string += " DEFAULT "
            if isinstance(self.__default, str):
                if self.__default_raw:
                    return_string += self.__default
                else:
                    return_string += "'{}'".format(self.__default)
            elif isinstance(self.__default, int):
                return_string += str(self.__default)
            elif isinstance(self.__default, bool):
                return_string += '"True"' if self.__default else '"False"'
        return return_string

    def get_default_value(self) -> str:
        '''returns the default blank to use for when not null on column'''
        if self.__variable_types[self.__variable_type] == 0:
            return "False"
        if self.__variable_types[self.__variable_type] == 1:
            return "0"
        if self.__variable_types[self.__variable_type] == 2:
            return "''"
        if self.__variable_types[self.__variable_type] == 3:
            return time.strftime('%Y-%m-%d')
        if self.__variable_types[self.__variable_type] == 4:
            return time.strftime('%H:%M:%S')
        if self.__variable_types[self.__variable_type] == 5:
            return time.strftime('%Y-%m-%d %H:%M:%S')
        if self.__variable_types[self.__variable_type] == 6:
            return time.strftime('%Y-%m-%d %H:%M:%S')
        if self.__variable_types[self.__variable_type] == 7:
            return time.strftime('%Y')
        if self.__variable_types[self.__variable_type] == 10:
            return "''"
        return ""

    def compare(self, to_compare) -> bool:
        '''Compare the results'''
        if to_compare.name != self.__name \
                or to_compare.variable_type != self.__variable_type \
                or to_compare.primary_key != self.__primary_key \
                or to_compare.not_null != self.__not_null:
            return False
        if self.__default is None:
            return True
        if to_compare.default != self.__default:
            return False
        return True
