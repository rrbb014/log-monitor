import os
import yaml

from glob import glob


class FilterManager:
    def __init__(self):
        self.filter_dict = {}

        filter_files = glob('*.yml')
        for f in filter_files:
            filter_name, _ = os.path.splitext(f)
            with open(f) as reader:
                temp_dict = yaml.safe_load(reader)

            self.filter_dict[filter_name] = temp_dict

    @property
    def predpipe(self):
        return self.filter_dict.get('predpipe')

    @property
    def confsync(self):
        return self.filter_dict.get('predpipe')
