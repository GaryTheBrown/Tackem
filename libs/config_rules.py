'''Config Rules'''

class ConfigRules:
    ''' Data for any group rules'''

    def __init__(self, many=False, for_each=None):
        # Defaults
        self._many = many
        self._for_each = None

        #Setup Group Rules bellow
        if isinstance(for_each, (list, dict)):
            self._for_each = for_each
            self._many = True

    def __repr__(self):
        '''print return'''
        return "ConfigRules(MANY=" + str(self._many) + ")"

    def many(self):
        '''return if the group is __many__'''
        return self._many

    def for_each(self):
        '''return the list to show for each'''
        return self._for_each
