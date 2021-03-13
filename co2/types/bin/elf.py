from abc import ABC, abstractmethod

class Elf(ABC):
    MAGIC_NUMBER = -1

    @abstractmethod
    def text():
        pass

