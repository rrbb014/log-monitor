import os
import yaml

from glob import glob


class FilterManager(dict):
    def __init__(self):
        self._filter_dict = {}
        target_path = os.path.join(os.path.dirname(__file__),'*.yml')
        filter_files = glob(target_path)
        for f in filter_files:
            filter_name, _ = os.path.splitext(os.path.split(f)[1])
            with open(f) as reader:
                temp_dict = yaml.safe_load(reader)

            self._filter_dict[filter_name] = temp_dict

    def __getattr__(self, key):
        return self._filter_dict[key]

    def __getitem__(self, key):
        return self._filter_dict[key]
