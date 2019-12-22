'''Input Attributes'''
from typing import Any

class InputAttributes:
    '''Input Attributes'''

    __kwargs = [
        "size", "maxlength", "height", "width", "list", "min", "max", "pattern",
        "placeholder", "step", "alt"
    ]


    def __init__(
            self,
            *args,
            **kwargs
    ):
        self.__autofocus = False
        self.__readonly = False
        self.__disabled = False
        self.__multiple = False
        self.__required = False
        self.__dict = {}

        for arg in args:
            if arg == "autofocus":
                self.__autofocus = True
            elif arg == "readonly":
                self.__readonly = True
            elif arg == "disabled":
                self.__disabled = True
            elif arg == "multiple":
                self.__multiple = True
            elif arg == "required":
                self.__required = True

        #kwargs for key:value ones with data- accepted
        for key, value in kwargs.items():
            if key[0:5] == "data_" or key in self.__kwargs:
                self.__dict[key] = str(value)


    def needed(self, *args):
        '''checks if the items are set otherwise raises an exception'''
        missing_list = []
        for arg in args:
            # if arg == "autofocus" and self.__autofocus:

            # elif arg == "readonly" and self.__readonly:

            # elif arg == "disabled" and self.__disabled:

            # elif arg == "multiple" and self.__multiple:

            # elif arg == "required" and self.__required:
            if arg not in self.__dict:
                missing_list.append(arg)

        if missing_list:
            raise ValueError("MISSING ARGUMENTS: " + ", ".join(missing_list))


    def block(self, *args):
        '''checks if any of the items are set and raises an exception if so'''
        block_list = []
        for arg in args:
            if (arg == "autofocus" and self.__autofocus) \
            or (arg == "readonly" and self.__readonly) \
            or (arg == "disabled" and self.__disabled) \
            or (arg == "multiple" and self.__multiple) \
            or (arg == "required" and self.__required) \
            or (arg in self.__dict):
                block_list.append(arg)

        if block_list:
            raise ValueError("BLOCKED ARGUMENTS FOUND: " + ", ".join(block_list))


    @property
    def config_spec(self) -> str:
        '''Returns the line for the config option'''
        variable_count = False
        return_string = ""

        _min = self.__dict.get('min', None)
        if _min:
            return_string += "min=" + str(_min)
            variable_count = True
        _max = self.__dict.get('max', None)
        if _max:
            if variable_count:
                return_string += ", "
            return_string += "max=" + str(_max)
        return return_string


    def html(self) -> str:
        '''returns html ready string'''
        string = ""

        for key, value in self.__dict.items():
            string += " " + key.replace("_", "-") + '="' + value + '"'


        if self.__autofocus:
            string += " autofocus"
        if self.__readonly:
            string += " readonly"
        if self.__disabled:
            string += " disabled"
        if self.__multiple:
            string += " multiple"
        if self.__required:
            string += " required"

        return string


    def get(self, key, default=None) -> Any:
        '''returns a value in the dictonary'''
        return self.__dict.get(key, default)


    def __getitem__(self, key) -> Any:
        '''[] getter'''
        return self.__dict.get(key, None)


    def __setitem__(self, key, value):
        '''[] setter'''
        self.__dict[key] = value


    def __iter__(self):
        '''getter itteration'''
        return iter(self.__dict)


    def __len__(self) -> int:
        return len(self.__dict)


    @property
    def autofocus(self) -> bool:
        '''returns if autofocus'''
        return self.__autofocus


    @property
    def readonly(self) -> bool:
        '''returns if read only'''
        return self.__readonly


    @property
    def disabled(self) -> bool:
        '''returns if disabled'''
        return self.__disabled


    @property
    def multiple(self) -> bool:
        '''returns multiple'''
        return self.__multiple


    @property
    def required(self) -> bool:
        '''returns if required'''
        return self.__required
