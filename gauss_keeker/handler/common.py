import re


class RegexRepository:

    def string_to_dict(self, string, pattern):
        try:
            regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)
            values = list(re.search(regex, string).groups())
            keys = re.findall(r'{(.+?)}', pattern)
            _dict = dict(zip(keys, values))
            return _dict
        except AttributeError:
            # TODO: To handling multi-line log, it may be deleted
            _dict = dict(message=string)
            return _dict

