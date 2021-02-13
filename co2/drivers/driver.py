from abc import ABC, abstractmethod

class Driver(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


