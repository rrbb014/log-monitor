
from gauss_keeker.common import RegexRepository
from .handler import Handler


class PredPipeHandler(Handler):

    def __init__(self, _filter: dict, logger=None):
        self._regex_repo = RegexRepository()
        self._filter = _filter
        self.event_list = list(self._filter.keys())
        self.logger = logger

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
            patterns = self._filter.get(event).get('pattern')
            if not type(patterns) == list:
                continue

            for fmt in patterns:
                sub_matched = self._regex_repo.check_matched(message, fmt)
                temp_list.append(sub_matched)

            matched = any(temp_list)
            matched_list.append((event, matched))

        # For handling exceptional case(2 more matched event label)
        cnt = 0
        event_label = []
        for event, matched in matched_list:
            if matched:
                event_label.append(event)
                cnt += 1

        if cnt == 1:
            return event_label[0]
        elif cnt > 1:
            raise Exception("2 more matched event label. labels: %s message: %s" % (' '.join(event_label), message))
        else:
            self.logger.warning("No matched label. Check filter pattern. message: %s" % message)
            return 'NOTFOUND'

    def handle(self, text) -> dict :
        """ Return log event label based on filter rule"""
        parse_dict = self._parse(text)
        self.logger.debug(parse_dict)

        message = parse_dict.get('message')
        event_label = self._classify(message)

        copy_dict = parse_dict.copy()

        if event_label != 'NOTFOUND':
            copy_dict.pop('message')

        copy_dict.pop('filename')
        copy_dict.pop('levelname')
        copy_dict.pop('lineno')

        tmp_label =  self._filter.get(event_label, False)
        if tmp_label:
            extract = tmp_label.get('extract', False)
        else: 
            extract = False

        if extract is None or not extract:
            copy_dict['event_label'] = event_label
            return copy_dict

        else:
            patterns = self._filter[event_label].get('pattern')
            extracted_dict = None
            for pattern in patterns:
                if extracted_dict is not None:
                    break

                extracted_dict = self._regex_repo.string_to_dict(message, pattern)

            copy_dict.update(extracted_dict)
            copy_dict['event_label'] = event_label
            return copy_dict

    def close(self):
        pass
