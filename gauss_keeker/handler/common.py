import re


class RegexRepository:

    def string_to_dict(self, string, pattern):
        # Thanks to url:
        # https://stackoverflow.com/questions/11844986/convert-or-unformat-a-string-to-variables-like-format-but-in-reverse-in-p/11849360#11849360
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

