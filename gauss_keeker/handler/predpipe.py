
from gauss_keeker.common import RegexRepository
from .handler import Handler

class EventClassifier:
    """
    Read text and classify event_label
    TODO Long-term: can be done by LDA model

    event_label list:
    """
    def __init__(self):
        self.event_list = [
                'EMPTY_DATA',
                'INITIALIZE:start_logger',
                'INTIIALIZE:print_args',
                'INITIALIZE:try_connect_zk',
                'INITIALIZE:zk_connected',
                'INITIALIZE:choose_pipeline_conf',
                'INITIALIZE:initialize_hdfsclient',
                'INITIALIZE:make_hdfs_output_dir',
                'INITIALIZE:connect_kafka',
                'INITIALIZE:update_process_component',
                'READ:reading_kafka_msg',
                'SKIP',
            ]
        pass
    
    def _abstract_initialize_event(self, text):
        INITIALIZE_START_LOGGER_RULE = "start logger"
        # TODO define more rule


    def classify(self, text: str) -> str:
        # TODO Do something

        return event_label


class PredPipeHandler(Handler):

    def __init__(self):
        self._regex_repo = RegexRepository()


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
        log_format = "{asctime} - {levelname} - {filename} - {lineno} - {message}"
        parse_dict = self._regex_repo.string_to_dict(text, log_format)
        return parse_dict

    def _classify(self, message):
        """ Classify log event to some Category"""
        
        pass

    def handle(self, text):
        parse_dict = self._parse(text)
        message = parse_dict.get('message')
        event_label = self._classify(message)

    def close(self):
        pass
