"""lib Base odd functions go here that don't have other places to go"""


def lower_keys(x):
    """Function to convert all keys to lower case in a dict"""
    if isinstance(x, list):
        return [lower_keys(v) for v in x]
    elif isinstance(x, dict):
        return {k.lower(): lower_keys(v) for k, v in x.items()}
    else:
        return x


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))
