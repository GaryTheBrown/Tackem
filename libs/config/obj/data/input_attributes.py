'''Input Attributes'''

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
            if key[0:5] == "data-" or key in self.__kwargs:
                self.__dict[key] = str(value)


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


    def html(self):
        '''returns html ready string'''
        string = ""

        for key, value in self.__dict.items():
            string += " " + key + '="' + value + '"'


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

    def get(self, key, default=None):
        '''returns a value in the dictonary'''
        return self.__dict.get(key, default)


    def __getitem__(self, key):
        '''[] getter'''
        return self.__dict.get(key, None)


    def __setitem__(self, key, value):
        '''[] setter'''
        self.__dict[key] = value


    def __iter__(self):
        '''getter itteration'''
        return iter(self.__dict)

    def __len__(self):
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
