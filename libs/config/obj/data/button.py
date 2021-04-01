"""Button"""
from typing import Any


class Button:
    """Button"""

    def __init__(self, label: str, action: str, append: bool, **kwargs: Any):
        if not isinstance(label, str):
            raise ValueError("label is not a String")
        if not isinstance(action, str):
            raise ValueError("action is not a String")
        if not isinstance(append, bool):
            raise ValueError("label is not a Boolean")

        self.__label = label
        self.__action = action
        self.__kwargs = kwargs
        self.__append = append

    def html_dict(self) -> dict:
        """returns the required Data for the html template to use"""
        data = [f"data-click-action={self.__action}"]
        for key, value in self.__kwargs.items():
            data.append(f"data-{key}={value}")
        return_dict = {
            "append": self.__append,
            "label": self.__label,
            "data": " ".join(data),
        }

        return return_dict
