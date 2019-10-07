import re
from copy import copy



class RegexRepository:

    def __init__(self):
        self.log_format = "{asctime} - {levelname} - {filename} - {lineno} - {message}"

    def check_matched(self, string, pattern):
        regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)

        searched = re.search(regex, string)
        if searched:
            values = list(searched.groups())
        else:
            values = []
        keys = re.findall(r'{(.+?)}', pattern)
        abstract_string = copy(string)
        for k, v in zip(keys, values):
            abstract_string = abstract_string.replace(v, '{'+k+'}', 1)

        matched = bool(re.findall(pattern, abstract_string)) 
        return matched

    def string_to_dict(self, string, pattern):
        # Thanks to url:
        # https://stackoverflow.com/questions/11844986/convert-or-unformat-a-string-to-variables-like-format-but-in-reverse-in-p/11849360#11849360
        try:
            # TODO: Cannot parse multi-line error log. Because of newline(\n).
            regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)
            values = list(re.search(regex, string).groups())
            keys = re.findall(r'{(.+?)}', pattern)
            _dict = dict(zip(keys, values))

            return _dict
        except AttributeError:
            self.logger.exception('AttributeError occured. message: %s, pattern: %s' % (string, pattern))
        except:
            self.logger.exception("Unexpected error occured. Maybe cannot search. message: %s, pattern: " % (string, pattern))
