from abc import ABCMeta, abstractmethod

class Handler(metaclass=ABCMeta):

    @abstractmethod
    def handle(self):
        pass

    @abstractmethod
    def close(self):
        pass
