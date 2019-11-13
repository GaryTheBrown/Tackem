'''Config Rules'''
from typing import Union


class ConfigRules:
    ''' Data for any group rules'''


    def __init__(self, many: bool = False, for_each: Union[list, dict] = None):
        # Defaults
        self.__many = many
        self.__for_each = None

        #Setup Group Rules bellow
        if isinstance(for_each, (list, dict)):
            self.__for_each = for_each
            self.__many = True


    def __repr__(self) -> str:
        '''print return'''
        return "ConfigRules(MANY=" + str(self.__many) + ")"


    @property
    def many(self) -> str:
        '''return if the group is __many__'''
        return self.__many


    @property
    def for_each(self) -> Union[list, dict]:
        '''return the list to show for each'''
        return self.__for_each
