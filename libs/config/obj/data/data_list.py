"""Config Object Data List"""


class DataList:
    """Config Object Data List"""

    def __init__(self, *options: str):
        if not all([isinstance(x, str) for x in options]):
            raise ValueError("One of the Data List Options is not a string")

        self.__options = options

    def html_dict(self, variable_name: str) -> dict:
        """returns the required Data for the html template to use"""
        return {"var_name": variable_name + "list", "values": self.__options}
