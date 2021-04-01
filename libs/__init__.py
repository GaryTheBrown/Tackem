"""lib Base odd functions go here that don't have other places to go"""


def lower_keys(x):
    """Function to convert all keys to lower case in a dict"""
    if isinstance(x, list):
        return [lower_keys(v) for v in x]
    elif isinstance(x, dict):
        return {k.lower(): lower_keys(v) for k, v in x.items()}
    else:
        return x
