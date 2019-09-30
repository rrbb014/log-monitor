
from gauss_keeker.common import RegexRepository
from .handler import Handler


class PredPipeHandler(Handler):

    def __init__(self, _filter: dict):
        self._regex_repo = RegexRepository()
        self._filter = _filter
        self.event_list = list(self._filter.keys())

    def _parse(self, text) -> dict:
        """
        Description:
        Parse text based on format 

        Keyword Arguments:
        text -- str, not parsed log text
        
        Return:
        parse_dict -- dict, parsed dictionary

        Example of return:
        {
            'asctime': '2019-02-19 10:51:38,733',
            'filename': 'entry_point.py',
            'level': 'INFO',
            'lineno': '153',
            'message': "choosing ./shared/confAT0221-sixteen-jupiter-glucose-eight12.json among ['/shared/confAT0221-sixteen-jupiter-glucose-eight12.json']"
        }
        """
        log_format = self._regex_repo.log_format
        parse_dict = self._regex_repo.string_to_dict(text, log_format)
        return parse_dict

    def _classify(self, message) -> str :
        """ Classify log event to some Category"""
        matched_list = []
        for event in self.event_list:
            temp_list = []
            patterns = self._filter.get(event)['pattern']
            assert type(patterns) == list

            for fmt in patterns:
                parsed = self._regex_repo.string_to_dict(message, fmt, match_check=True)
                sub_matched = parsed.get('matched', False)
                temp_list.append(sub_matched)

            matched = any(temp_list)
            matched_list.append(matched)

        # For handling exceptional case(2 more matched event label)
        cnt = 0
        event_label = []
        for event, matched in zip(self.event_list, matched_list):
            if matched:
                event_label.append(event)
                cnt += 1

        if cnt == 1:
            return event_label[0]
        elif cnt > 1:
            print(event_label)
            raise Exception("2 more matched event label. labels: %s" % ' '.join(event_label))
        else:
            raise Exception("No matched label. Check filter pattern. message: %s" % message)

    def handle(self, text):
        parse_dict = self._parse(text)
        message = parse_dict.get('message')
        event_label = self._classify(message)

    def close(self):
        pass
