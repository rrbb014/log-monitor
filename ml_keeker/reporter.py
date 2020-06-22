import pandas as pd
from abc import ABCMeta, abstractmethod


class StatusReporter(metaclass=ABCMeta):

    @abstractmethod
    def report(self):
        pass

    @abstractmethod
    def close(self):
        pass


class FileStatusReporter(StatusReporter):
    def __init__(self, status_rootpath: str, output_rootpath: str, logger):
        # do something
        pass
        
    def report(self):
        # do something
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
