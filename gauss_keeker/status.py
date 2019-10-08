import os
import io
import time
import yaml
import pandas as pd

from collections import OrderedDict

# TODO: Should it be splitted into abstract class and child class?
predpipe_header=['asctime', 'event_label', 'pipeline_id', 'kafka_topic', 'max_latency', 'kafka_start', 'timezone', 'duration', 'timeout', 'expected', 'pushed', 'max_buffer_size', 'now_msg_time', 'loop', 'traceback']

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

        stat_dict = cur_stat.update(stat_dict)

        with open(self._store_path, 'w+', encoding='utf8') as writer:
            yaml.safe_dump(stat_dict, writer)

        self.store_time = time.time()
        if self.logger:
            self.logger.info("Stored state")
        else:
            print("Stored state")

    def _summarize(self, _buffer: list, last_state: dict) -> dict:
        buffer_obj = io.StringIO('\n'.join(_buffer))
        df = pd.read_table(buffer_obj, names=predpipe_header)

        from IPython import embed;embed()

        stat_dict = {}

        # TODO; EMPTYDATA time duration
        # All emptydata
        # emptydata-> read -> emptydata
        #'READ-reading_kafka_msg' 
        t_df = df[df['event_label'] == 'READ-reading_kafka_msg']
        if len(t_df) == 0:
            df.iloc[0].asctime

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

        state_dict = kwargs
        ordered_values = [state_dict.get(header, 'None') for header in predpipe_header]
        stat = "\t".join(ordered_values)
        self._buffer.append(stat)


    def close(self):
        del self._buffer
