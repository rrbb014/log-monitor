import os
import io
import time
import random
import json

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
    def __init__(
            self,
            store_rootpath: str,
            name: str,
            max_buffer_size=1000,
            timeout=60*5,
            logger=None):

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
            with open(self._store_path, 'w+', encoding='utf8') as writer:
                writer.write('')
                self.store_time = time.time()

    def _read(self) -> dict:
        pass

    def _write(self) -> None:
        write_lines = ""
        for line in self._buffer:
            write_lines += line+"\n"

        with open(self._store_path, 'a+', encoding="utf8") as writer:
            writer.write(write_lines)

        self._buffer = []
        self.store_time = time.time()

    def store(self, data_dict, eof=False) -> bool:
        now = time.time()

        # randomly report current stat-buffer size
        trial = random.random()
        if trial <= 0.01:
            self.logger.info("StatusManager Buffer: {buf}/{max_size}".format(
                buf=len(self._buffer),
                max_size=self.max_buffer_size
            ))

        if len(self._buffer) > self.max_buffer_size or now - self.store_time > self.timeout:
            self.logger.debug("try to write")
            self._write()
            return True

        store_value = json.dumps(data_dict)
        if data_dict["event_label"].lower() not in ["notfound", "skip", "skippable"]:
            self._buffer.append(store_value)

        if eof:
            self.logger.debug("try to write")
            self._write()
            return True

        return False

    def close(self):
        del self._buffer
