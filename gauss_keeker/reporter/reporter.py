from abc import ABCMeta, abstractmethod

class StatusReporter(metaclass=ABCMeta):

    @abstractmethod
    def report(self):
        pass

    @abstractmethod
    def close(self):
        pass
