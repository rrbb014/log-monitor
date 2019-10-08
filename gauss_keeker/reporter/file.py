import pandas as pd

from .reporter import StatusReporter

class FileStatusReporter(StatusReporter):
    def __init__(self, status_rootpath: str, output_rootpath: str, logger):
        # do something
        pass
        
    def report(self):
        # do something
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
