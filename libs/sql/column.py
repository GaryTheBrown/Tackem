'''Column Defenition Stuff Useful for updating tables'''
import time

class Column:
    '''Column'''
    variable_types = {
        "bit":0,#bool
        "tinyint":1, "smallint":1, "int":1, "mediumint":1, "integer":1, "bigint":1,#ints
        "real":1, "double":1, "float":1, "decimal":1, "numeric":1,#ints
        "char":2, "varchar":2, "binary":2, "varbinary":2, "tinyblob":2, "blob":2,#text
        "mediumblob":2, "longblob":2, "tinytext":2, "text":2, "mediumtext":2, "longtext":2,#text
        #special
        "date":3, "time":4, "timestamp":5, "datetime":6, "year":7, "enum":8, "set":9, "json":10
    }
    def __init__(self, name, variable_type=False, primary_key=False,
                 unique=False, not_null=False, default=None, default_raw=False):

        if isinstance(name, str):
            self.name = name
            self.variable_type = variable_type
            self.primary_key = bool(primary_key)
            self.unique = bool(unique)
            self.not_null = bool(not_null)
            self.default = default
            self.default_raw = bool(default_raw)
        else:
            self.name = name[1]
            self.variable_type = name[2]
            self.primary_key = bool(name[5])
            self.not_null = bool(name[3])
            self.default = name[4]

    def to_string(self):
        '''turns Column info into a string for commands'''
        return_string = '"' + self.name + '"'
        return_string += " "
        return_string += self.variable_type
        if self.primary_key:
            return_string += " PRIMARY KEY"
        if self.not_null:
            return_string += " NOT NULL"
        if self.unique:
            return_string += " UNIQUE"
        if not self.default is None:
            return_string += " DEFAULT "
            if isinstance(self.default, str):
                if self.default_raw:
                    return_string += self.default
                else:
                    return_string += "'" + self.default + "'"
            elif isinstance(self.default, int):
                return_string += self.default
            elif isinstance(self.default, bool):
                if self.default:
                    return_string += "True"
                else:
                    return_string += "False"
        return return_string

    def get_default_value(self):
        '''returns the default blank to use for when not null on column'''
        return_string = ""
        if self.variable_types[self.variable_type] == 0:
            return_string += "False"
        elif self.variable_types[self.variable_type] == 1:
            return_string += "0"
        elif self.variable_types[self.variable_type] == 2:
            return_string += "''"
        elif self.variable_types[self.variable_type] == 3:
            return_string += time.strftime('%Y-%m-%d')
        elif self.variable_types[self.variable_type] == 4:
            return_string += time.strftime('%H:%M:%S')
        elif self.variable_types[self.variable_type] == 5:
            return_string += time.strftime('%Y-%m-%d %H:%M:%S')
        elif self.variable_types[self.variable_type] == 6:
            return_string += time.strftime('%Y-%m-%d %H:%M:%S')
        elif self.variable_types[self.variable_type] == 7:
            return_string += time.strftime('%Y')
        elif self.variable_types[self.variable_type] == 10:
            return_string += "''"
        return return_string
    def compare(self, to_compare):
        '''Compare the results'''
        if not to_compare.name == self.name:
            return False
        if not to_compare.variable_type == self.variable_type:
            return False
        if not to_compare.primary_key == self.primary_key:
            return False
        if not to_compare.not_null == self.not_null:
            return False
        if self.default is None:
            return True
        if not to_compare.default == self.default:
            return False
        return True