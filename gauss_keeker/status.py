import os
import io
import time
import yaml

from datetime import datetime

# TODO: Should it be splitted into abstract class and child class?
predpipe_header=[
        'asctime',
        'event_label',
        'pipeline_id',
        'kafka_topic',
        'max_latency',
        'kafka_start',
        'timezone',
        'duration',
        'timeout',
        'expected',
        'pushed',
        'max_buffer_size',
        'now_msg_time',
        'loop',
        'traceback',
        'message',
    ]

def str_to_datetime(string):
    datetime_obj = datetime.strptime(string, '%Y-%m-%d %H:%M:%S,%f')
    return datetime_obj

class StatusManager:
    """Store status"""
    def __init__(self, store_rootpath: str, name: str, max_buffer_size=100, timeout=60*5, logger=None):
        self._store_rootpath = store_rootpath
        self._name = name
        self.logger = logger
        self.max_buffer_size=max_buffer_size
        self.timeout= timeout
        self._buffer = []

        if not os.path.exists(store_rootpath):
            os.makedirs(store_rootpath, exist_ok=True)

        self._store_path = os.path.join(store_rootpath, name) + '.status'

        # Load storage file
        
        if os.path.exists(self._store_path):
            self.store_time = time.time()

        else:
            with open(self._store_path, 'w+') as writer:
                writer.write('')
                self.store_time = time.time()

    def _read(self) -> dict:
        with open(self._store_path) as reader:
            cur_stat = yaml.safe_load(reader)

        return cur_stat

    def _write(self, _buffer) -> None:
        last_stat = self._read()
        stat_dict = self._summarize(_buffer, last_stat)
        self._buffer = []

        stat_dict = last_stat.update(stat_dict)

        with open(self._store_path, 'w+', encoding='utf8') as writer:
            yaml.safe_dump(stat_dict, writer)

        self.store_time = time.time()
        if self.logger:
            self.logger.info("Stored state")
        else:
            print("Stored state")

    def _summarize(self, _buffer: list, last_state: dict) -> dict:

        stat_dict = {}

        for event in _buffer:
            if event['event_label'] == "INIT-connect_kafka":
                stat_dict['kafka_topic'] = event['kafka_topic']
                stat_dict['kafka_consumer_config'] = event['config']
                stat_dict['pipeline_id'] = event['pipeline_id']
                continue

            if event['event_label'] == "INIT-update_component":
                stat_dict['max_latency'] = event['max_latency']
                stat_dict['pipeline_id'] = event['pipeline_id']
                continue

            # available scenario: All emptydata
            # emptydata-> read -> emptydata
            if event['event_label'] == "EMPTYDATA":
                if last_state.get('begin_empty_data', None) is None:
                    stat_dict['begin_empty_data'] = event['asctime']

                stat_dict['end_empty_data'] = event['asctime']
                continue

            if event['event_label'] == "READ-reading_kafka_msg":
                stat_dict['begin_empty_data'] = None
                stat_dict['end_empty_data'] = None

                poll_duration = stat_dict.get('poll_duration', []) 
                poll_duration.append(event['duration'])
                stat_dict['poll_duration'] = poll_duration

                stat_dict['timeout'] = event['timeout']
                continue

            if event['event_label'] == "READ-poll_time":
                poll_duration = stat_dict.get('poll_duration', []) 
                poll_duration.append(event['duration'])
                stat_dict['poll_duration'] = poll_duration
                stat_dict['timeout'] = event['timeout']

                    


        # TODO; EMPTYDATA time duration
        #'READ-reading_kafka_msg' 
        #stat_dict['emptydata_duration'] =        

        # TODO: how calculate ? 
        # TODO: now does it exist kafka_topic?
        # TODO: when is last poll time?
        # TODO: average throughput
        # TODO: latency check
        raise NotImplementedError

        return stat_dict

    def store(self, **kwargs):
        now = time.time()
        if len(self._buffer) > self.max_buffer_size or now - self.store_time > self.timeout:
            self._write(self._buffer)
            return 

        self._buffer.append(kwargs)


    def close(self):
        del self._buffer
