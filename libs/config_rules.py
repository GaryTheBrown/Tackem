'''Config Rules'''


class ConfigRules:
    ''' Data for any group rules'''


    def __init__(self, many=False, for_each=None):
        # Defaults
        self.__many = many
        self.__for_each = None

        #Setup Group Rules bellow
        if isinstance(for_each, (list, dict)):
            self.__for_each = for_each
            self.__many = True


    def __repr__(self):
        '''print return'''
        return "ConfigRules(MANY=" + str(self.__many) + ")"


    def many(self):
        '''return if the group is __many__'''
        return self.__many


    def for_each(self):
        '''return the list to show for each'''
        return self.__for_each
