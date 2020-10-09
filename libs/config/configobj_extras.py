'''configobj Extra Checks'''
import re
from validate import ValidateError

def email(value):
    '''validator for emails'''
    if len(value) > 7:
        if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", value) is not None:
            return value
    raise ValidateError(f'"{value}" is not an email address')

EXTRA_FUNCTIONS = {
    "email": email
}
