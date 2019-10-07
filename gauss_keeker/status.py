import os
import yaml

from collections import OrderedDict

class StatusManager:
    """Store status"""
    def __init__(self, store_rootpath: str, name: str, logger):
        self._store_rootpath = store_rootpath
        self._name = name
        self.logger = logger

        if not os.path.exists(store_rootpath):
            os.makedirs(store_rootpath, exist_ok=True)

        self._store_path = os.path.join(store_rootpath, name) + '.yml'

        # Load storage file
        if os.path.exists(self._store_path):
            self._state_reader = open(self._store_path)
            self._status = yaml.safe_load(self._state_reader)
        else:
            with open(self._store_path, 'w+') as writer:
                tmp = dict(name=self._name, empty_sequence=[], states=[])
                yaml.safe_dump(tmp, writer)
                self._state_reader = open(self._store_path)
                self._status = tmp.copy()

        self._state_writer = None

    def store(self, **kwargs):
        state_dict = kwargs
        event_label = state_dict.get('event_label')

        # Store
        self._status['states'].append(state_dict)
        if event_label == 'EMPTYDATA':
            self._status['empty_sequence'].append(state_dict['asctime'])

        if self._state_writer is None:
            self._state_writer = open(self._store_path, 'w')

        # TODO: weird store file. should be changed
        yaml.safe_dump(self._status, self._state_writer)

        self.logger.info("Stored state")

    def close(self):
        self._state_reader.close()
        self._state_writer.close()
