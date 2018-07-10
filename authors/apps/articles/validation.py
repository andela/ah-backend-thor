import re
from rest_framework.exceptions import APIException


class Validator:

    def letter_starts(field, value):
        if re.compile('[a-zA-Z]+').match(value):
            return value
        else:
            raise APIException({
                'error': f'Field {field}; Must start with a letter!'
            })
