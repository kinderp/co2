from abc import ABCMeta, abstractmethod
from co2.system_calls import IOSystemCalls


class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def init(argsubparsers):
        pass

    @abstractmethod
    def execute(args):
        pass


