'''Config Rules'''
from typing import Union


class ConfigRules:
    ''' Data for any group rules'''


    def __init__(self, for_each: Union[list, dict] = None):
        # Defaults
        self.__for_each = None

        #Setup Group Rules bellow
        if isinstance(for_each, (list, dict)):
            self.__for_each = for_each


    @property
    def for_each(self) -> Union[list, dict]:
        '''return the list to show for each'''
        return self.__for_each
