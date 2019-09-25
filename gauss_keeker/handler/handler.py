from abc import ABCMeta, abstractmethod

# TODO: Add AbstractClass for additional handler in the future
class Handler(metaclass=ABCMeta):

    @abstractmethod
    def handle(self):
        pass

    @abstractmethod
    def close(self):
        pass
