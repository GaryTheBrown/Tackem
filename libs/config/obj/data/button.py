'''Button'''
from libs.html_system import HTMLSystem
class Button():
    '''Button'''

    def __init__(self, label: str, action: str, append: bool, **kwargs):
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


    @property
    def html(self) -> str:
        '''returns the buttons html'''
        data = 'data-action="{}"'.format(self.__action)
        for key, value in self.__kwargs.items():
            data += ' data-{}="{}"'.format(key, value)
        return HTMLSystem.part(
            "inputs/button_append" if self.__append else "input/button",
            LABEL=self.__label,
            DATA=data,
        )